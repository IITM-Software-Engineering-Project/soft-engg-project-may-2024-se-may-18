import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
import sys, os
from local_db import TestBase, test_engine, TestSessionLocal
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import app  # Import your FastAPI app
from sqlalchemy.orm import Session
from database.models import Course, CourseEnrollment, User, Module, Assignment, AssignmentMarks, Exam, Lecture
from datetime import datetime
from resources.instructor import get_db  # Adjust the import path as necessary
from sqlite3 import IntegrityError

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
        user = User(id=1, username="testuser", role="instructor", last_login=datetime.now(), email="test@example.com", password="testpass")
        test_db.add(user)
        test_db.commit()
        
        course = Course(id=1, title="Test Course", description="Test Description", total_modules=10, price=100.0)
        test_db.add(course)
        test_db.commit()
        
        module = Module(id=1, title="Test Module", total_lectures=5, total_assignments=3, course_id=course.id, description="Test Description")
        test_db.add(module)
        test_db.commit()

        lecture = Lecture(id=1, title="Test Lecture", module_id=module.id, url="http://example.com", transcript="Lecture Transcript")
        test_db.add(lecture)
        test_db.commit()
        
        assignment = Assignment(id=1, module_id=module.id, title="Test Assignment", type="homework", due_date=datetime.now())
        test_db.add(assignment)
        test_db.commit()
        
        enrollment = CourseEnrollment(student_id=user.id, course_id=course.id, enrollment_date=datetime.now())
        test_db.add(enrollment)
        test_db.commit()
        
        exam = Exam(id=1, course_id=course.id, student_id=user.id, exam_id=1, marks=90.0)
        test_db.add(exam)
        test_db.commit()
        yield test_db
    finally:
        test_db.close()
        TestBase.metadata.drop_all(bind=test_engine)
        TestBase.metadata.create_all(bind=test_engine)


def test_add_module_success(setup_test_data):
    data = {"title": "New Module", "description": "Module Description", "total_lectures": 6, "course_id": 1}
    response = client.post("/add_module", json=data)
    assert response.status_code == 200
    assert response.json() == {"message": "Module added successfully"}

def test_add_module_invalid_courseid(setup_test_data):
    data = {"title": "New Module", "description": "Module Description", "total_lectures": 6, "course_id": 2}
    response = client.post("/add_module", json=data)
    assert response.status_code == 404
    assert response.json() == {"detail": "Course not found"}

def test_edit_module_success(setup_test_data):
    data = {"title": "Updated Module Title"}
    response = client.put("/edit_module/1", json=data)
    assert response.status_code == 200
    assert response.json() == {"message": "Module updated successfully"}

def test_edit_module_not_found(setup_test_data):
    data = {"title": "Updated Module Title"}
    response = client.put("/edit_module/999", json=data)
    assert response.status_code == 404
    assert response.json() == {"detail": "Content not found"}

def test_delete_module_success(setup_test_data):
    response = client.delete("/delete_module/1")
    assert response.status_code == 200
    assert response.json() == {"message": "Module deleted successfully"}

def test_delete_module_not_found(setup_test_data):
    response = client.delete("/delete_module/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Module not found"}

def test_add_lecture_success(setup_test_data):
    data = {"title": "New Lecture", "module_id": 1, "url": "http://example.com", "transcript": "Lecture Transcript"}
    response = client.post("/add_lecture", json=data)
    assert response.status_code == 200
    assert response.json() == {"message": "Lecture added successfully"}

def test_add_lecture_invalid_moduleid(setup_test_data):
    data = {"title": "New Lecture", "module_id": 999, "url": "http://example.com", "transcript": "Lecture Transcript"}
    response = client.post("/add_lecture", json=data)
    assert response.status_code == 404
    assert response.json() == {"detail": "Module not found"}



def test_edit_lecture_success(setup_test_data):
    data = {"title": "Updated Lecture Title"}
    
    response = client.put("/edit_lecture/1", json=data)
    assert response.status_code == 200
    assert response.json() == {"message": "lecture updated successfully"}

def test_edit_lecture_not_found(setup_test_data):
    data = {"title": "Updated Lecture Title"}
    response = client.put("/edit_lecture/999", json=data)
    assert response.status_code == 404
    assert response.json() == {"detail": "lecture not found"}

def test_delete_lecture_success(setup_test_data):
    response = client.delete("/delete_lecture/1")
    assert response.status_code == 200
    assert response.json() == {"message": "lecture deleted successfully"}

def test_delete_lecture_not_found(setup_test_data):
    response = client.delete("/delete_lecture/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "lecture not found"}


def test_add_assignment_success(setup_test_data):
    data = {"id":2,"title": "New Assignment", "description": "Assignment Description", "module_id": 1, "type": "homework", "due_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}    
    response = client.post("/add_assignment", json=data)
    assert response.status_code == 200
    assert response.json() == {"message": "assignment added successfully"}

def test_add_assignment_invalid_moduleid(setup_test_data):
    data = {"id":2,"title": "New Assignment", "description": "Assignment Description", "module_id": 999, "type": "homework", "due_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    response = client.post("/add_assignment", json=data)
    assert response.status_code == 404
    assert response.json() == {"detail": "Module not found"}

def test_edit_assignment_success(setup_test_data):
    data = {"title": "Updated Assignment Title"}
    response = client.put("/edit_assignment/1", json=data)
    assert response.status_code == 200
    assert response.json() == {"message": "assignment updated successfully"}

def test_edit_assignment_not_found(setup_test_data):
    data = {"title": "Updated Assignment Title"}
    response = client.put("/edit_assignment/999", json=data)
    assert response.status_code == 404
    assert response.json() == {"detail": "assignment not found"}

def test_edit_assignment_invalid_moduleid(setup_test_data):
    data = {"module_id": 999}
    response = client.put("/edit_assignment/1", json=data)
    assert response.status_code == 404
    assert response.json() == {"detail": "Module not found"}

def test_delete_assignment_success(setup_test_data):
    response = client.delete("/delete_assignment/1")
    assert response.status_code == 200
    assert response.json() == {"message": "assignment deleted successfully"}

def test_delete_assignment_not_found(setup_test_data):
    response = client.delete("/delete_assignment/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "assignment not found"}

# def test_add_exam_success(setup_test_data):
#     data = {"course_id": 1, "student_id": 1, "exam_id": 2, "marks": 90.0}
#     response = client.post("/add_exam", json=data)
#     assert response.status_code == 200
#     assert response.json() == {"message": "Exam added successfully"}