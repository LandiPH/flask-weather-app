import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    assert 'message' in response.json
    assert response.json['message'] == 'Flask Weather API'

def test_health(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json['status'] == 'healthy'

def test_status(client):
    response = client.get('/status')
    assert response.status_code == 200
    assert response.json['app'] == 'flask-weather-app'
    assert response.json['status'] == 'running'

def test_weather_invalid_city(client):
    response = client.get('/weather?city=xyznonexistentcity123')
    assert response.status_code == 404

def test_weather_valid_city(client):
    response = client.get('/weather?city=London')
    assert response.status_code in [200, 500]  # 200 if API available, 500 if network issue
    if response.status_code == 200:
        assert 'city' in response.json
        assert 'temperature' in response.json
