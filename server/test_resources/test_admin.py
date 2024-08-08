import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
import sys, os
from local_db import TestBase, test_engine, TestSessionLocal
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import app
from database.models import Course
from api.payload_schema.payloadschema import CourseCreate, CourseUpdate, CourseResponse
from resources.admin import get_db

# Override dependency for testing
def get_test_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()
        
app.dependency_overrides[get_db] = get_test_db
client = TestClient(app)

# Test setup
@pytest.fixture(scope="module")
def setup_test_data():
    # Create schema
    TestBase.metadata.create_all(bind=test_engine)
    
    db = TestSessionLocal()
    
    # Setup test data
    # db.query(Course).delete()  # Clear all courses before adding test data
    test_course = Course(id=1, title='Test Course', description='A test course description', total_modules=10, price=100.0)
    db.add(test_course)
    db.commit()
    
    yield db
    
    # Teardown
    db.query(Course).delete()  # Clean up after tests
    db.commit()
    TestBase.metadata.drop_all(bind=test_engine)  # Drop all tables

def test_create_course(setup_test_data):
    response = client.post("/courses/create", json={
        "title": "New Test Course 1",
        "description": "A new test course description",
        "total_modules": 10,
        "price": 100.0
    })
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New Test Course 1"
    assert data["description"] == "A new test course description"

def test_update_course(setup_test_data):
    response = client.put("/courses/update", json={
        "id": 1,
        "title": "Updated Test Course",
        "description": "An updated test course description"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Test Course"
    assert data["description"] == "An updated test course description"

def test_delete_course(setup_test_data):
    response = client.delete("/courses/delete", params={"id": 1})
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Course deleted successfully"

def test_get_course(setup_test_data):
    setup_test_data.query(Course).filter(Course.id == 1).first()

    response = client.get("/courses/get?id=1")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Course"
    assert data["description"] == "A test course description"

def test_get_all_courses(setup_test_data):
    response = client.get("/courses/list")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["title"] == "New Test Course 1"
    assert data[0]["description"] == "A new test course description"