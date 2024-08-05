from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
import os
import sys
from datetime import datetime
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dotenv import load_dotenv
import pytest
from fastapi.testclient import TestClient

from database.models import User, Assignment, CourseEnrollment, Course, Module, Exam, AssignmentMarks  # Adjust import based on your models
from main import app
load_dotenv()

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
    """Set up test data."""
    created_ids = {
        'course': 106,
        'module': 106,
        'assignment': 106,
        'assignment_marks': 106,
        'exam': 106,
        'enrollment': 106,
        'student': 106
    }
    user = User(id=created_ids['student'], username="Test Student", email="test@student.com", last_login=datetime.now(), role='student', password='test')  # Adjust based on your User model
    db_session.add(user)
    # Add test data
    course = Course(id=created_ids['course'], title="Introduction to Programming", description="Learn the basics of programming", total_modules=5, price=299.99)
    db_session.add(course)
    
    module = Module(id=created_ids['module'], course_id=created_ids['course'], title="Module 1: Basics", description="Introduction to basic concepts", total_lectures=10, total_assignments=3)
    db_session.add(module)

    db_session.commit()

    assignment = Assignment(id=created_ids['assignment'], module_id=created_ids['module'], title="Assignment 1", description="Basic assignment", type="Homework", due_date=datetime.now())
    db_session.add(assignment)
    db_session.commit()
    assignment_marks = AssignmentMarks(
        id=created_ids['assignment_marks'],
        assignment_id=created_ids['assignment'],
        student_id=created_ids['student'],
        marks=85,
        submitted_at=datetime.now(),  # Provide a valid datetime
        graded_at=datetime.now(),     # Provide a valid datetime if required
        feedback="Good job!"         # Provide feedback if required
    )    
    db_session.add(assignment_marks)

    exam = Exam(exam_id=created_ids['exam'], course_id=created_ids['course'], student_id=created_ids['enrollment'], marks=78)
    db_session.add(exam)

    enrollment = CourseEnrollment(student_id=created_ids['enrollment'], course_id=created_ids['course'], enrollment_date=datetime.now())
    db_session.add(enrollment)

    db_session.commit()

    yield db_session

    # Teardown code: remove test data
    db_session.query(CourseEnrollment).filter_by(student_id=created_ids['enrollment']).delete()
    db_session.query(AssignmentMarks).filter_by(id=created_ids['assignment_marks']).delete()
    db_session.query(Exam).filter_by(exam_id=created_ids['exam']).delete()
    db_session.query(Assignment).filter_by(id=created_ids['assignment']).delete()
    db_session.query(Exam).filter_by(exam_id=created_ids['exam']).delete()
    db_session.query(Module).filter_by(id=created_ids['module']).delete()
    db_session.query(Course).filter_by(id=created_ids['course']).delete()
    db_session.query(Exam).filter_by(exam_id=created_ids['exam']).delete()
    db_session.query(User).filter_by(id=created_ids['student']).delete()
    db_session.commit()


# FastAPI TestClient
client = TestClient(app)

# Example test functions
def test_get_student_course_overview_valid(setup_db):
    response = client.get(f"/student/enrolled_course/student-overview?course_id={106}&student_id={106}")
    assert response.status_code == 200
    print(response.json())
    assert response.json() == {
        "course_description": "Learn the basics of programming",
        "assignment_marks": {
            "106": 85
        },
        "exam_marks": {
            "106": 78
        }
    }

def test_enroll_student(setup_db):
    """
    To ensure that the student can be enrolled in a course successfully and the enrollment is stored correctly in the database.
    """
    payload = {
        "student_id": 107,
        "course_id": 107
    }

    # Make the POST request to enroll the student
    response = client.post("/student/enroll", json=payload)
    
    # Assert the response status and message
    assert response.status_code == 200
    assert response.json() == {"message": "Enrollment successful"}

    # Verify the student was enrolled in the course
    enrollment = setup_db.query(CourseEnrollment).filter_by(student_id=107, course_id=107).first()
    setup_db.query(CourseEnrollment).filter_by(student_id=107, course_id=107).delete()
    assert enrollment is not None

if __name__ == "__main__":
    pytest.main()
