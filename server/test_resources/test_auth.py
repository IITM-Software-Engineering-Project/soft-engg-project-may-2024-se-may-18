import pytest
from fastapi.testclient import TestClient
import os,sys
from sqlalchemy.orm import sessionmaker
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database.models import User
from main import app  # Import your FastAPI app
from resources.auth import get_db
from datetime import datetime
from local_db import TestBase, test_engine, TestSessionLocal
import bcrypt
# Dependency override for tests
SECRET_KEY = 'secret-key'
ALGORITHM = "HS256"
def get_test_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()
app.dependency_overrides[get_db] = get_test_db
client = TestClient(app)

@pytest.fixture(scope="function")
def setup_test_data():
    # Setup: create a new session and add test data
    test_db = TestSessionLocal()
    try:
        # Add your test data here
        password = "testpassword"
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user = User(username="testuser", role="instructor", last_login=datetime.now(), email="test@example.com", password=hashed_password.decode('utf-8'))
        test_db.add(user)
        test_db.commit()
    
        yield test_db
    finally:
        test_db.close()
        TestBase.metadata.drop_all(bind=test_engine)
        TestBase.metadata.create_all(bind=test_engine)


# Test case for user registration
def test_register_success():
    response = client.post("/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword",
        "role": "student"
    })
    assert response.status_code == 200
    assert response.json() == {"message": "User registered successfully"}

def test_register_user_already_exists(setup_test_data):
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
def test_login_success(setup_test_data):
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

def test_login_incorrect_password(setup_test_data):
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

def test_login_user_not_found():
    response = client.post("/login", json={
        "username": "nonexistentuser",
        "password": "testpassword"
    })
    assert response.status_code == 400
    assert response.json() == {"detail": "Incorrect username or password"}
