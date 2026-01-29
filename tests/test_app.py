import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_page(client):
    """Test if the index page loads successfully"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Flask CI/CD Pipeline' in response.data

def test_api_status(client):
    """Test the status API endpoint"""
    response = client.get('/api/status')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'success'
    assert 'message' in data
    assert 'timestamp' in data

def test_api_health(client):
    """Test the health check endpoint"""
    response = client.get('/api/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert 'service' in data

def test_api_info(client):
    """Test the info endpoint"""
    response = client.get('/api/info')
    assert response.status_code == 200
    data = response.get_json()
    assert data['app'] == 'Flask CI/CD Demo'
    assert 'version' in data