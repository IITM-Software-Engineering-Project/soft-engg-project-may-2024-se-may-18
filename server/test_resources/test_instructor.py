import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
import sys, os
from local_db import TestBase, test_engine, TestSessionLocal
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import app  # Import your FastAPI app
from sqlalchemy.orm import Session
from database.models import Course, CourseEnrollment, User, Module, Assignment, AssignmentMarks, Exam, Lecture, AssignmentQuestion
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

        assignmentQuestion = AssignmentQuestion(options={"a":1,"b":2,"c":3,"d":4}, answer="a", question="Who are you?", assignment_id="1")
        test_db.add(assignmentQuestion)
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

def test_add_question_success(setup_test_data):#Not there
    data = {"question": "What is the capital of France?", "assignment_id": 1, "options":{"1":"a","2":"b","3":"c","4":"d"},"answer":"1"}
    response = client.post("/add_question", json=data)
    assert response.status_code == 200
    assert response.json() == {"message": "Question added successfully"}

def test_add_question_failure_missing_fileds(setup_test_data):
    data = {"question": "What is the capital of France?"}
    response = client.post("/add_question", json=data)
    assert response.status_code == 400
    assert response.json() == {"detail": "Missing fields in payload"}

def test_edit_question_success(setup_test_data):
    data = {"question_text": "Updated question text"}
    response = client.put("/edit_question/1", json=data)
    assert response.status_code == 200
    assert response.json() == {"message": "question updated successfully"}

def test_edit_question_not_found(setup_test_data):
    data = {"question": "Updated question text"}
    response = client.put("/edit_question/999", json=data)
    
    assert response.status_code == 404
    assert response.json() == {"detail": "question not found"}

def test_edit_question_invalid_data(setup_test_data):
    # Assuming text is a required field
    data = {}
    response = client.put("/edit_question/1", json=data)
    
    assert response.status_code == 422
    assert response.json().get("detail") is not None

def test_delete_question_success(setup_test_data):
    response = client.delete("/delete_question/1")
    
    assert response.status_code == 200
    assert response.json() == {"message": "question deleted successfully"}

    # Verify the deletion in the database
    question = setup_test_data.query(AssignmentQuestion).filter(AssignmentQuestion.id == 1).first()
    setup_test_data.commit()
    assert question is None

def test_delete_question_not_found(setup_test_data):
    response = client.delete("/delete_question/999")
    
    assert response.status_code == 404
    assert response.json() == {"detail": "question not found"}

def test_get_enrolled_students_success(setup_test_data):
    response = client.get("/instructor/enrolled-students/1")
    
    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "username": "testuser"},
    ]

def test_get_enrolled_students_no_students(setup_test_data):
    # Remove all students from course_id 1
    
    response = client.get("/instructor/enrolled-students/999")
    
    assert response.status_code == 200
    assert response.json() == []

def test_get_enrolled_students_course_not_found(setup_test_data):
    response = client.get("/instructor/enrolled-students/999")
    
    assert response.status_code == 200
    assert response.json() == []

def test_create_exam_success(setup_test_data):

    response = client.post("/instructor/create-exam?course_id=1&exam_id=101")
    
    assert response.status_code == 200
    assert response.json() == {"message": "Exam created successfully for all enrolled students"}
    
    # Verify exams are created
    # Assuming there are 2 enrolled students

def test_create_exam_invalid_course_id(setup_test_data):
    response = client.post("/instructor/create-exam?course_id=101&exam_id=10")
    
    assert response.status_code == 404
    assert response.json() == {"detail": "course not found"}


def test_grade_exam_success(setup_test_data):
    # Assume course_id=1, student_id=1, exam_id=101, and marks=85.0
    response = client.put("/instructor/grade-exam", params={
        "course_id": 1,
        "student_id": 1,
        "exam_id": 1,
        "marks": 85.0
    })
    
    assert response.status_code == 200
    assert response.json() == {"message": "Exam graded successfully"}

def test_grade_exam_not_found(setup_test_data):
    # Assume course_id=1, student_id=1, exam_id=999, and marks=85.0 (exam_id=999 does not exist)
    response = client.put("/instructor/grade-exam", params={
        "course_id": 1,
        "student_id": 1,
        "exam_id": 999,
        "marks": 85.0
    })
    
    assert response.status_code == 404
    assert response.json() == {"detail": "Exam not found"}

def test_get_course_progress_success(setup_test_data):
    # Assume course_id=1 and student_id=1
    response = client.get("/course-progress", params={
        "course_id": 1,
        "student_id": 1
    })
    
    assert response.status_code == 200
    
    progress = response.json()
    assert "assignment_progress" in progress
    assert "exam_progress" in progress
    assert "overall_progress" in progress
    
    # Verify that the values are within the expected range
    assert 0 <= progress["assignment_progress"] <= 100
    assert 0 <= progress["exam_progress"] <= 100
    assert 0 <= progress["overall_progress"] <= 100


def test_get_course_progress_no_assignments_or_exams(setup_test_data):
    # Assume course_id=1 and student_id=1 where there are no assignments or exams
    response = client.get("/course-progress", params={
        "course_id": 1,
        "student_id": 1
    })
    
    assert response.status_code == 200
    
    progress = response.json()
    assert progress["assignment_progress"] == 0
    assert progress["exam_progress"] == 100
    assert progress["overall_progress"] == 50
