from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, JSON, ForeignKey

# Define the test database URL
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"

# Create the engine for the test database
test_engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False})

# Define the session local for the test database
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

# Define the TestBase for the test database
TestBase = declarative_base()

# Define models (same as in your main db setup)
class User(TestBase):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False)
    role = Column(String(50), nullable=False)
    last_login = Column(DateTime, nullable=False)
    email = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)



class Course(TestBase):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    description = Column(String(500), nullable=False)
    total_modules = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    # modules = relationship("Module", back_populates="course")

class CourseInstructor(TestBase):
    __tablename__ = 'course_instructors'

    id = Column(Integer, primary_key=True, autoincrement=True)
    instructor_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)


class CourseEnrollment(TestBase):
    __tablename__ = 'course_enrollments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    enrollment_date = Column(DateTime, nullable=False)


class Transaction(TestBase):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    amount = Column(Float, nullable=False)
    date = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    transaction_type = Column(String(50))
    description = Column(String(255))
    status = Column(String(50))


class Module(TestBase):
    __tablename__ = 'modules'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    total_lectures = Column(Integer, nullable=False)
    total_assignments = Column(Integer, nullable=False)
    description = Column(String(500), nullable=True)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    # course = relationship("Course", back_populates="modules")
    # assignments = relationship("Assignment", back_populates="module")
    # lectures = relationship("Lecture", back_populates="module")

class Lecture(TestBase):
    __tablename__ = 'lectures'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    module_id = Column(Integer, ForeignKey('modules.id'), nullable=False)
    url = Column(String(255), nullable=False)
    transcript = Column(Text, nullable=True)
    # module = relationship("Module", back_populates="lectures")


class Assignment(TestBase):
    __tablename__ = 'assignments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    module_id = Column(Integer, ForeignKey('modules.id'), nullable=False)
    title = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)
    type = Column(String(50), nullable=False)
    due_date = Column(DateTime, nullable=False)
    # module = relationship("Module", back_populates="assignments")
    # questions = relationship("AssignmentQuestion", back_populates="assignment")
    # marks = relationship("AssignmentMarks", back_populates="assignment")


class AssignmentQuestion(TestBase):
    __tablename__ = 'assignment_questions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    assignment_id = Column(Integer, ForeignKey(
        'assignments.id'), nullable=False)
    image = Column(String(255), nullable=True)
    question = Column(Text, nullable=False)
    options = Column(JSON, nullable=False)
    answer = Column(String(100), nullable=False)
    # assignment = relationship("Assignment", back_populates="questions")

class AssignmentMarks(TestBase):
    __tablename__ = 'assignment_marks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    assignment_id = Column(Integer, ForeignKey('assignments.id'), nullable=False)
    student_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    marks = Column(Float, nullable=False)
    submitted_at = Column(DateTime, nullable=False)
    graded_at = Column(DateTime, nullable=True)
    feedback = Column(Text, nullable=True)
    # assignment = relationship("Assignment", back_populates="marks")
    # student = relationship("User")

class Exam(TestBase):
    __tablename__ = 'exams'

    id = Column(Integer, primary_key=True, autoincrement=True)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    student_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    exam_id = Column(Integer, nullable=False)
    marks = Column(Float, nullable=True)
TestBase.metadata.create_all(bind=test_engine)
# import pytest
# from fastapi.testclient import TestClient
# from unittest.mock import MagicMock
# import os, sys
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# from main import app
# from resources.student import get_db
# mock_session = MagicMock()

# def override_get_db():
#     try:
#         yield mock_session
#     finally:
#         pass

# app.dependency_overrides[get_db] = override_get_db

# @pytest.fixture
# def mock_db_session():
#     return mock_session
