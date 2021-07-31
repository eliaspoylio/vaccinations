from fastapi.testclient import TestClient

from app.app import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"backend": "Hello world!"}

def test_show_orders_arrived_count():
    response = client.get("/orders/count")
    assert response.status_code == 200
    assert response.json() == [{"count": 5000}]

def test_show_vaccinations_count():
    response = client.get("/vaccinations/count")
    assert response.status_code == 200
    assert response.json() == [{"count": 7000}]

def test_show_orders_arrived_total():
    response = client.get("/orders/total/2021-04-12T11:10:06")
    assert response.status_code == 200
    assert response.json() == [{"count": 5000}]

def test_show_vaccinations_arrived_total():
    response = client.get("/vaccinations/total/2021-04-12T11:10:06")
    assert response.status_code == 200
    assert response.json() == [{"sum": 25015}]

def test_show_vaccinations_used_day():
    response = client.get("/vaccinations/used/2021-01-05")
    assert response.status_code == 200
    assert response.json() == [{"sum": 8}]

def test_show_orders_expired_day():
    response = client.get("/orders/expired/2021-04-12T11:10:06.473587Z")
    assert response.status_code == 200
    assert response.json() == [{"count": 3482}]

def test_show_vaccinations_expired_day():
    response = client.get("/vaccinations/expired/2021-04-12T11:10:06.473587Z")
    assert response.status_code == 200
    assert response.json() == [{"sum": 12590}]

def test_show_vaccinations_left_day():
    response = client.get("/vaccinations/left/2021-04-12T11:10:06.473587Z")
    assert response.status_code == 200
    assert response.json() == [{"sum": 123456789}]

def test_show_orders_arrived_day():
    response = client.get("/orders/day/2021-03-20")
    assert response.status_code == 200
    assert response.json() == [{"count": 61}]

def test_show_orders_manufacturer_total_day():
    response = client.get("/orders/manufacturer/total/2021-04-12T11:10:06.473587Z")
    assert response.status_code == 200
    assert response.json() == [{"vaccine":"SolarBuddhica","sum":10056},{"vaccine":"Zerpfy","sum":8315},{"vaccine":"Antiqua","sum":6644}]