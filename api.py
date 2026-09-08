from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from typing import Literal
from datetime import datetime, timezone

app=FastAPI(title='Property & BPO Management API',version='2.0.0')
properties=[]; work_orders=[]
class Property(BaseModel): address:str=Field(min_length=3); city:str; client:str; status:Literal['new','active','completed','on_hold']='new'
class WorkOrder(BaseModel): property_id:int=Field(gt=0); vendor:str; task:str; priority:Literal['low','medium','high']='medium'; status:Literal['open','assigned','in_progress','completed']='open'
@app.get('/health')
def health(): return {'status':'ok','service':'property-bpo-management','version':'2.0.0'}
@app.post('/properties')
def add_property(p:Property):
    item={'id':len(properties)+1,**p.model_dump(),'created_at':datetime.now(timezone.utc).isoformat()}; properties.append(item); return item
@app.get('/properties')
def list_properties(): return properties
@app.post('/work-orders')
def add_work_order(w:WorkOrder):
    item={'id':len(work_orders)+1,**w.model_dump(),'created_at':datetime.now(timezone.utc).isoformat()}; work_orders.append(item); return item
@app.get('/work-orders')
def list_work_orders(): return work_orders
@app.patch('/work-orders/{order_id}')
def update_work_order(order_id:int,status:Literal['open','assigned','in_progress','completed']):
    for x in work_orders:
        if x['id']==order_id:x['status']=status;return x
    return {'error':'work order not found'}
@app.get('/dashboard')
def dashboard():
    return {'properties':len(properties),'work_orders':len(work_orders),'open_work_orders':sum(x['status']!='completed' for x in work_orders),'high_priority':sum(x['priority']=='high' for x in work_orders)}
app.mount('/',StaticFiles(directory='web',html=True),name='web')
