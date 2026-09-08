from fastapi.testclient import TestClient
from api import app
client=TestClient(app)
def test_health(): assert client.get('/health').status_code==200
def test_dashboard():
    r=client.get('/dashboard'); assert r.status_code==200; assert 'properties' in r.json()
