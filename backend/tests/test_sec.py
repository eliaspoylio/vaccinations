from fastapi.testclient import TestClient

from app.app import app

client = TestClient(app, raise_server_exceptions=False)

def test_legit_date():
    response = client.get("/orders/expired/20210303")
    assert response.status_code == 200

def test_sql_injection():
    response = client.get("/orders/expired/20210303 or (1=1)")
    assert response.status_code == 500