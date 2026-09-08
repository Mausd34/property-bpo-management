from fastapi.testclient import TestClient
from api import app
client=TestClient(app)
def test_health(): assert client.get('/health').json()['status']=='ok'
def test_dashboard():
    r=client.get('/dashboard'); assert r.status_code==200; assert 'work_orders' in r.json()
