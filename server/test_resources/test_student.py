import pytest
from fastapi.testclient import TestClient
import sys, os
from local_db import TestBase, test_engine, TestSessionLocal
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import app  # Import your FastAPI app
from sqlalchemy.orm import Session
from database.models import Course, CourseEnrollment, User, Module, Assignment, AssignmentMarks, Exam
from datetime import datetime
from resources.student import get_db
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
        user = User(id = 1, username="testuser", role="student", last_login=datetime.now(), email="test@example.com", password="testpass")
        test_db.add(user)
        test_db.commit()
        # Create and add test data
        course = Course(id=1,title="Test Course", description="Test Description", total_modules=10, price=100.0)
        test_db.add(course)
        test_db.commit()
        
        module = Module(title="Test Module", total_lectures=5, total_assignments=3, course_id=course.id, description="Test Description")
        test_db.add(module)
        test_db.commit()
        
        enrollment = CourseEnrollment(student_id=user.id, course_id=course.id, enrollment_date=datetime.now())
        test_db.add(enrollment)
        test_db.commit()
        
        assignment = Assignment(module_id=module.id, title="Test Assignment", type="homework", due_date=datetime.now())
        test_db.add(assignment)
        test_db.commit()
        
        exam = Exam(course_id=course.id, student_id=user.id, exam_id=1, marks=90.0)
        test_db.add(exam)
        test_db.commit()

        yield test_db
    finally:
        test_db.close()
        # Clean up the test database
        TestBase.metadata.drop_all(bind=test_engine)
        TestBase.metadata.create_all(bind=test_engine)

# Test the API endpoint
def test_get_student_course_overview(setup_test_data):
    # Test successful response
    response = client.get("/student/enrolled_course/student-overview?course_id=1&student_id=1")
    assert response.status_code == 200
    data = response.json()
    assert data["course_description"] == "Test Description"
    assert data["assignment_marks"] == {'1': None}
    assert data["exam_marks"] == {'1': 90.0}

    # Test with invalid course_id
    response = client.get("/student/enrolled_course/student-overview?course_id=999&student_id=1")
    assert response.status_code == 404
    assert response.json() == {"detail": "Enrollment not found"}

    # Test with invalid student_id
    response = client.get("/student/enrolled_course/student-overview?course_id=1&student_id=999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Enrollment not found"}

    # Test with both invalid course_id and student_id
    response = client.get("/student/enrolled_course/student-overview?course_id=999&student_id=999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Enrollment not found"}

def test_get_module_details(setup_test_data):
    # Test successful response
    response = client.get("/student/enrolled_course/?course_id=1&module_id=1")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Module"
    assert data["total_lectures"] == 5
    assert data["total_assignments"] == 3

    # Test with invalid course_id
    response = client.get("/student/enrolled_course/?course_id=999&module_id=1")
    assert response.status_code == 404
    assert response.json() == {"detail": "Module not found"}

    # Test with invalid module_id
    response = client.get("/student/enrolled_course/?course_id=1&module_id=999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Module not found"}

    # Test with both invalid course_id and module_id
    response = client.get("/student/enrolled_course/?course_id=999&module_id=999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Module not found"}

def test_get_course_details_success(setup_test_data):
    response = client.get("/student/courses/1")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Course"
    assert data["description"] == "Test Description"
    assert data["total_modules"] == 10
    assert data["price"] == 100.0

def test_get_course_details_invalid_course_id(setup_test_data):
    response = client.get("/student/courses/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Course not found"}

def test_enroll_student_success(setup_test_data):
    response = client.post("/student/enroll", json={"student_id": 1, "course_id": 2})
    assert response.status_code == 200
    assert response.json() == {"message": "Enrollment successful"}


def test_get_enrolled_courses_success(setup_test_data):
    response = client.get("/student/enrolled-courses/1")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == 1
    assert data[0]["title"] == "Test Course"

def test_get_enrolled_courses_invalid_student_id(setup_test_data):
    response = client.get("/student/enrolled-courses/999")
    assert response.status_code == 200
    assert response.json() == []

def test_get_enrolled_courses_no_courses(setup_test_data):
    # First, clear existing enrollments
    setup_test_data.query(CourseEnrollment).delete()
    setup_test_data.commit()

    response = client.get("/student/enrolled-courses/1")
    assert response.status_code == 200
    assert response.json() == []  # Assuming no courses are enrolled for this student


def test_enroll_student_success(setup_test_data):
    course = Course(id=2, title="Test Course 2", description="Test Description 2", total_modules=10, price=100.0)
    setup_test_data.add(course)
    setup_test_data.commit()
    response = client.post("/student/enroll", json={"student_id": 1, "course_id": 2})
    setup_test_data.query(Course).filter(Course.id == 2).delete()
    setup_test_data.commit()
    assert response.status_code == 200
    assert response.json() == {"message": "Enrollment successful"}

def test_enroll_student_invalid_student_id(setup_test_data):
    response = client.post("/student/enroll", json={"student_id": 999, "course_id": 1})
    assert response.status_code == 404
    assert response.json() == {"detail": "Student or Course not found"}

def test_enroll_student_invalid_course_id(setup_test_data):
    response = client.post("/student/enroll", json={"student_id": 1, "course_id": 999})
    assert response.status_code == 404
    assert response.json() == {"detail": "Student or Course not found"}

def test_enroll_student_invalid_ids(setup_test_data):
    response = client.post("/student/enroll", json={"student_id": 999, "course_id": 999})
    assert response.status_code == 404
    assert response.json() == {"detail": "Student or Course not found"}

def test_enroll_student_already_enrolled(setup_test_data):
    response = client.post("/student/enroll", json={"student_id": 1, "course_id": 1})
    assert response.status_code == 400  # Assuming a conflict status code
    assert response.json() == {"detail": "Student is already enrolled in the course"}
