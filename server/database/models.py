from sqlalchemy import JSON, Column, Float, ForeignKey, Integer, String, DateTime, Text
from sqlalchemy.orm import declarative_base, sessionmaker
from database.db_sql import init_db

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False)
    role = Column(String(50), nullable=False)
    last_login = Column(DateTime, nullable=False)
    email = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)


class Course(Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    description = Column(String(500), nullable=False)
    total_modules = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)


class CourseInstructor(Base):
    __tablename__ = 'course_instructors'

    id = Column(Integer, primary_key=True, autoincrement=True)
    instructor_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)


class CourseEnrollment(Base):
    __tablename__ = 'course_enrollments'

    student_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    course_id = Column(Integer, ForeignKey('courses.id'), primary_key=True)
    enrollment_date = Column(DateTime, nullable=False)


class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    amount = Column(Float, nullable=False)
    date = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    transaction_type = Column(String(50))
    description = Column(String(255))
    status = Column(String(50))


class Module(Base):
    __tablename__ = 'modules'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    total_lectures = Column(Integer, nullable=False)
    total_assignments = Column(Integer, nullable=False)
    description = Column(String(500), nullable=True)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)


class Lecture(Base):
    __tablename__ = 'lectures'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    module_id = Column(Integer, ForeignKey('modules.id'), nullable=False)
    url = Column(String(255), nullable=False)
    transcript = Column(Text, nullable=True)


class Assignment(Base):
    __tablename__ = 'assignments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    module_id = Column(Integer, ForeignKey('modules.id'), nullable=False)
    title = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)
    type = Column(String(50), nullable=False)
    due_date = Column(DateTime, nullable=False)


class AssignmentQuestion(Base):
    __tablename__ = 'assignment_questions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    assignment_id = Column(Integer, ForeignKey(
        'assignments.id'), nullable=False)
    image = Column(String(255), nullable=True)
    question = Column(Text, nullable=False)
    answer_choices = Column(JSON, nullable=False)
    answer = Column(String(100), nullable=False)

class AssignmentMarks(Base):
    __tablename__ = 'assignment_marks'
    id = Column(Integer, primary_key=True, autoincrement=True)
    assignment_id = Column(Integer, ForeignKey(
        'assignments.id'), nullable=False)
    student_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    assignment_answer = Column(Text, nullable = True)
    marks = Column(Float, nullable=False)
    submitted_at = Column(DateTime, nullable=False)
    graded_at = Column(DateTime, nullable=True)
    feedback = Column(Text, nullable=True)


class Exam(Base):
    __tablename__ = 'exams'

    id = Column(Integer, primary_key=True, autoincrement=True)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    student_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    exam_id = Column(Integer, nullable=False)
    marks = Column(Float, nullable=True)


engine = None
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
if not engine:
    engine = init_db()
    # Base.metadata.create_all(engine, checkfirst=True)
    session = sessionmaker(bind=engine)
    print("SQL Database connected Successfully.")


""" class Content(Base):
    __tablename__ = 'contents'

    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    week_no = Column(Integer, nullable=False)
    link = Column(String(50), nullable=False) """

