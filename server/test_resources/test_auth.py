import pytest
from fastapi.testclient import TestClient
import os,sys
from sqlalchemy.orm import sessionmaker
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database.models import User
from main import app  # Import your FastAPI app
from resources.auth import get_db

from local_db import TestBase, test_engine, TestSessionLocal

# Dependency override for tests

def get_test_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()
app.dependency_overrides[get_db] = get_test_db
client = TestClient(app)


# Test case for user registration
def test_register_success(client):
    response = client.post("/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword",
        "role": "student"
    })
    assert response.status_code == 200
    assert response.json() == {"message": "User registered successfully"}

def test_register_user_already_exists(client, setup_test_data):
    client.post("/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword",
        "role": "student"
    })
    response = client.post("/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword",
        "role": "student"
    })
    assert response.status_code == 400
    assert response.json() == {"detail": "User already exists"}

# Test case for login
def test_login_success(client, setup_test_data):
    client.post("/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword",
        "role": "student"
    })
    response = client.post("/login", json={
        "username": "testuser",
        "password": "testpassword"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_login_incorrect_password(client, setup_test_data):
    client.post("/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword",
        "role": "student"
    })
    response = client.post("/login", json={
        "username": "testuser",
        "password": "wrongpassword"
    })
    assert response.status_code == 400
    assert response.json() == {"detail": "Incorrect username or password"}

def test_login_user_not_found(client):
    response = client.post("/login", json={
        "username": "nonexistentuser",
        "password": "testpassword"
    })
    assert response.status_code == 400
    assert response.json() == {"detail": "Incorrect username or password"}
