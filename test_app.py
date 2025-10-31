import pytest
import json
from app import create_app, db
from app.models import User, Todo

@pytest.fixture
def client():
    """Create a test client with in-memory database"""
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["JWT_SECRET_KEY"] = "test-secret-key"

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()


@pytest.fixture
def auth_headers(client):
    """Register and login a test user to get JWT headers"""
    # Register user
    client.post("/auth/register", json={"username": "testuser", "password": "password"})
    # Login user
    res = client.post("/auth/login", json={"username": "testuser", "password": "password"})
    token = res.get_json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


# ---------------- AUTH TESTS ----------------

def test_register(client):
    res = client.post("/auth/register", json={"username": "user1", "password": "pass"})
    assert res.status_code == 201
    assert res.get_json()["message"] == "registered"


def test_register_duplicate(client):
    client.post("/auth/register", json={"username": "user1", "password": "pass"})
    res = client.post("/auth/register", json={"username": "user1", "password": "pass"})
    assert res.status_code == 409


def test_login(client):
    client.post("/auth/register", json={"username": "user1", "password": "pass"})
    res = client.post("/auth/login", json={"username": "user1", "password": "pass"})
    assert res.status_code == 200
    assert "access_token" in res.get_json()


# ---------------- TODOS TESTS ----------------

def test_create_todo(client, auth_headers):
    res = client.post("/api/todos", json={"title": "Test Todo"}, headers=auth_headers)
    assert res.status_code == 201
    data = res.get_json()
    assert data["title"] == "Test Todo"
    assert data["completed"] is False


def test_list_todos(client, auth_headers):
    # Add a todo
    client.post("/api/todos", json={"title": "Todo1"}, headers=auth_headers)
    res = client.get("/api/todos", headers=auth_headers)
    data = res.get_json()
    assert len(data) == 1
    assert data[0]["title"] == "Todo1"


def test_update_todo(client, auth_headers):
    # Add a todo
    res = client.post("/api/todos", json={"title": "Old Title"}, headers=auth_headers)
    todo_id = res.get_json()["id"]
    # Update todo
    res = client.patch(f"/api/todos/{todo_id}", json={"title": "New Title", "completed": True}, headers=auth_headers)
    data = res.get_json()
    assert data["title"] == "New Title"
    assert data["completed"] is True


def test_delete_todo(client, auth_headers):
    # Add a todo
    res = client.post("/api/todos", json={"title": "Delete Me"}, headers=auth_headers)
    todo_id = res.get_json()["id"]
    # Delete todo
    res = client.delete(f"/api/todos/{todo_id}", headers=auth_headers)
    assert res.status_code == 200
    assert res.get_json()["message"] == "deleted"


# ---------------- PAGE ROUTES TESTS ----------------

def test_home_page(client):
    res = client.get("/")
    assert res.status_code == 200
    assert b"<html" in res.data  # basic check for HTML


def test_login_page(client):
    res = client.get("/login")
    assert res.status_code == 200
    assert b"<html" in res.data


def test_register_page(client):
    res = client.get("/register")
    assert res.status_code == 200
    assert b"<html" in res.data
