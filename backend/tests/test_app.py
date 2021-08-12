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
    assert response.json() == [{"sum": 4090}]

def test_show_vaccinations_expiring_tendays():
    response = client.get("/vaccinations/expiring_tendays/20210223")
    assert response.status_code == 200
    assert response.json() == [{"sum": 1205}]

def test_show_orders_arrived_day():
    response = client.get("/orders/day/2021-03-20")
    assert response.status_code == 200
    assert response.json() == [{"count": 61}]

def test_show_manufacturer_total_day():
    response = client.get("/manufacturer/total/2021-04-12T11:10:06.473587Z")
    assert response.status_code == 200
    assert response.json() == [{"vaccine":"Antiqua","orders":1661,"injections":6644},{"vaccine":"SolarBuddhica","orders":1676,"injections":10056},{"vaccine":"Zerpfy","orders":1663,"injections":8315}]

def test_show_district_total_day():
    response = client.get("/district/total/2021-01-06")
    assert response.status_code == 200
    assert response.json() == [{"healthcaredistrict":"HYKS","orders":66,"injections":333},{"healthcaredistrict":"KYS","orders":21,"injections":103},{"healthcaredistrict":"OYS","orders":21,"injections":106},{"healthcaredistrict":"TAYS","orders":33,"injections":163},{"healthcaredistrict":"TYKS","orders":25,"injections":124}]

def test_show_timeseries():
    response = client.get("/timeseries")
    assert response.status_code == 200