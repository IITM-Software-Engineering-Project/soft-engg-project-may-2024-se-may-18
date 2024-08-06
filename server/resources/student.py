from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker, Session
from database.models import Course, CourseEnrollment, User, Module, Assignment, AssignmentMarks, Exam
from database.db_sql import init_db
from api.payload_schema.payloadschema import CourseOverview, ModuleDetails, CourseDetails, EnrollmentResponse, CourseEnrolled, StudentEnrolled\
    , StudentCourseOverviewRequest, StudentModuleDetailsRequest
from datetime import datetime
from typing import List
# Initialize the database and create a session
# engine = init_db()
# Session = sessionmaker(bind=engine)
# session = Session()

def get_db():
    engine = init_db()
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

student_router = APIRouter()

# Student endpoints
@student_router.get("/student/enrolled_course/student-overview", response_model=CourseOverview,
                    description="Get an overview of the student's course including assignments and exam marks.",
                    tags=["Student"])
def get_student_course_overview(course_id: int, student_id: int, session: Session = Depends(get_db)):
    enrollment = session.query(CourseEnrollment).filter(
        CourseEnrollment.course_id == course_id,
        CourseEnrollment.student_id == student_id
    ).first()
    
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    
    course = session.query(Course).filter(Course.id == course_id).first()
    
    assignments = session.query(Assignment).join(Module).filter(Module.course_id == course_id).all()
    assignment_marks = {}
    for assignment in assignments:
        marks = session.query(AssignmentMarks).filter(
            AssignmentMarks.assignment_id == assignment.id,
            AssignmentMarks.student_id == student_id
        ).first()
        assignment_marks[assignment.id] = marks.marks if marks else None
    
    exams = session.query(Exam).filter(
        Exam.course_id == course_id,
        Exam.student_id == student_id
    ).all()
    exam_marks = {exam.exam_id: exam.marks for exam in exams}
    
    return CourseOverview(
        course_description=course.description,
        assignment_marks=assignment_marks,
        exam_marks=exam_marks
    )

@student_router.get("/student/enrolled_course/", response_model=ModuleDetails,
                    tags = ["Student"],
                    description="Get details of a module of the course.")
def get_module_details(course_id: int,module_id: int,  session: Session = Depends(get_db)):
    module = session.query(Module).filter(
        Module.course_id == course_id,
        Module.id == module_id
    ).first()
    
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    
    return ModuleDetails(
        title=module.title,
        description=module.description,
        total_lectures=module.total_lectures,
        total_assignments=module.total_assignments
    )

@student_router.get("/student/courses/{course_id}", response_model=CourseDetails,
                    tags = ["Student"],
                    description="Get details of a course.")
def get_course_details(course_id: int,  session: Session = Depends(get_db)):
    course = session.query(Course).filter(Course.id == course_id).first()
    
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return CourseDetails(
        title=course.title,
        description=course.description,
        total_modules=course.total_modules,
        price=course.price
    )


@student_router.post("/student/enroll", response_model=EnrollmentResponse,
                     tags = ["Student"],
                     description="Enroll a student in a course.")
def enroll_student(request: StudentCourseOverviewRequest,  session: Session = Depends(get_db)):
    student_id = request.student_id
    course_id = request.course_id
    enrollment = CourseEnrollment(
        student_id=student_id,
        course_id=course_id,
        enrollment_date=datetime.now()
    )
    session.add(enrollment)
    session.commit()
    return EnrollmentResponse(message="Enrollment successful")


@student_router.get("/student/enrolled-courses/{student_id}", response_model=List[CourseEnrolled],
                    tags = ["Student"],
                    description="Get the list of courses enrolled by a student.")
def get_enrolled_courses(student_id: int, session: Session = Depends(get_db)):
    enrollments = session.query(CourseEnrollment).filter(CourseEnrollment.student_id == student_id).all()
    course_ids = [enrollment.course_id for enrollment in enrollments]
    courses = session.query(Course).filter(Course.id.in_(course_ids)).all()
    return [CourseEnrolled(id=course.id, title=course.title) for course in courses]

