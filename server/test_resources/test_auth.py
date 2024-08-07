import os
import sys
from datetime import datetime
from unittest.mock import patch, MagicMock
from sqlalchemy.orm import sessionmaker
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine
# Add parent directory to path for module imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app
from database.models import User, session  # Adjust import based on your models

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# FastAPI TestClient
client = TestClient(app)

# Database setup
def init_db():
    try:
        engine = create_engine(os.getenv("DATABASE_SQL_URL"))
        return engine
    except SQLAlchemyError as e:
        print(f"Failed to create engine: {e}")
        raise

engine = init_db()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """Create a new database session for a test."""
    session = SessionLocal()
    try:
        yield session
    except Exception as e:
        print(f"An error occurred during the test: {e}")
        session.rollback()
        raise
    finally:
        session.rollback()
        session.close()

@pytest.fixture(scope="function")
def setup_db(db_session):
    """Set up test data for authentication."""
    user = User(username="existinguser", email="existinguser@example.com", password="hashedpassword", role="user")
    db_session.add(user)
    db_session.commit()

    yield db_session

    # Teardown code: remove test data
    db_session.query(User).filter_by(username="existinguser").delete()
    db_session.commit()

def test_register_user_success(setup_db):
    """Test user registration with valid data."""
    new_user_data = {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "password123",
        "role": "user"
    }

    response = client.post("/register", json=new_user_data)

    assert response.status_code == 200
    assert response.json() == {"message": "User registered successfully"}

def test_register_user_already_exists(setup_db):
    """Test user registration with an existing username."""
    existing_user_data = {
        "username": "existinguser",
        "email": "newemail@example.com",
        "password": "password123",
        "role": "user"
    }

    response = client.post("/register", json=existing_user_data)

    assert response.status_code == 400
    assert response.json() == {"detail": "User already exists"}

def test_register_integrity_error(setup_db):
    """Test user registration with integrity error (e.g., unique constraint violation)."""
    new_user_data = {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "password123",
        "role": "user"
    }

    with patch('database.models.SessionLocal') as mock:
        mock.return_value.__enter__.return_value.add.side_effect = IntegrityError("Mock IntegrityError", "params", "orig")
        response = client.post("/register", json=new_user_data)
    
    assert response.status_code == 400
    assert response.json() == {"detail": "Error registering user"}

if __name__ == "__main__":
    pytest.main()
