from fastapi import FastAPI,HTTPException,Depends
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from pydantic import BaseModel,Field
from typing import Literal
from datetime import datetime,timezone
from app.auth import hash_password,create_token,verify_token
from app.db import connect,init_db
app=FastAPI(title='Property & BPO Management API',version='4.0.0');init_db();security=HTTPBearer(auto_error=False)
properties=[];work_orders=[]
class Credentials(BaseModel):username:str=Field(min_length=3,max_length=80);password:str=Field(min_length=6,max_length=200)
class Property(BaseModel):address:str=Field(min_length=3);city:str;client:str;status:Literal['new','active','completed','on_hold']='new'
class WorkOrder(BaseModel):property_id:int=Field(gt=0);vendor:str;task:str;priority:Literal['low','medium','high']='medium';status:Literal['open','assigned','in_progress','completed']='open'
def current_user(c:HTTPAuthorizationCredentials=Depends(security)):
    if not c:raise HTTPException(401,'Authentication required')
    u=verify_token(c.credentials)
    if not u:raise HTTPException(401,'Invalid or expired token')
    return u
@app.get('/health')
def health():return {'status':'ok','service':'property-bpo-management','version':'4.0.0'}
@app.post('/auth/register')
def register(b:Credentials):
    with connect() as c:
        if c.execute('SELECT 1 FROM users WHERE username=?',(b.username,)).fetchone():raise HTTPException(409,'Username already exists')
        c.execute('INSERT INTO users(username,password_hash) VALUES(?,?)',(b.username,hash_password(b.password)));c.commit()
    return {'message':'registered','username':b.username}
@app.post('/auth/login')
def login(b:Credentials):
    with connect() as c:u=c.execute('SELECT * FROM users WHERE username=?',(b.username,)).fetchone()
    if not u or u['password_hash']!=hash_password(b.password):raise HTTPException(401,'Invalid username or password')
    return {'access_token':create_token(u['username']),'token_type':'bearer'}
@app.get('/auth/me')
def me(u=Depends(current_user)):return u
@app.post('/properties')
def add_property(p:Property,u=Depends(current_user)):
    item={'id':len(properties)+1,**p.model_dump(),'created_at':datetime.now(timezone.utc).isoformat()};properties.append(item);return item
@app.get('/properties')
def list_properties(u=Depends(current_user)):return properties
@app.post('/work-orders')
def add_work_order(w:WorkOrder,u=Depends(current_user)):
    item={'id':len(work_orders)+1,**w.model_dump(),'created_at':datetime.now(timezone.utc).isoformat()};work_orders.append(item);return item
@app.get('/work-orders')
def list_work_orders(u=Depends(current_user)):return work_orders
@app.patch('/work-orders/{order_id}')
def update_work_order(order_id:int,status:Literal['open','assigned','in_progress','completed'],u=Depends(current_user)):
    for x in work_orders:
        if x['id']==order_id:x['status']=status;return x
    raise HTTPException(404,'Work order not found')
@app.get('/dashboard')
def dashboard(u=Depends(current_user)):return {'properties':len(properties),'work_orders':len(work_orders),'open_work_orders':sum(x['status']!='completed' for x in work_orders),'high_priority':sum(x['priority']=='high' for x in work_orders)}
app.mount('/',StaticFiles(directory='web',html=True),name='web')
