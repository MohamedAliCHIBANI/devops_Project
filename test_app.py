import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    """Test the home route returns 200"""
    rv = client.get('/')
    assert rv.status_code == 200
    json_data = rv.get_json()
    assert json_data['status'] == "running"

def test_get_todos(client):
    """Test fetching the initial list of todos"""
    rv = client.get('/api/todos')
    assert rv.status_code == 200
    assert len(rv.get_json()['todos']) >= 2

def test_add_todo(client):
    """Test adding a new todo item"""
    new_task = {"title": "Test Automated Pipeline"}
    rv = client.post('/api/todos', json=new_task)
    assert rv.status_code == 201
    assert rv.get_json()['title'] == "Test Automated Pipeline"

def test_add_todo_invalid(client):
    """Test adding a todo without a title fails"""
    rv = client.post('/api/todos', json={})
    assert rv.status_code == 400