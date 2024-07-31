from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker
from database.models import Course, CourseEnrollment, User, Module, Assignment, AssignmentMarks, Exam
from database.db_sql import init_db
from api.payload_schema.payloadschema import CourseOverview, ModuleDetails, CourseDetails, EnrollmentResponse, CourseEnrolled, StudentEnrolled\
    , StudentCourseOverviewRequest, StudentModuleDetailsRequest
from datetime import datetime
from typing import List
# Initialize the database and create a session
engine = init_db()
Session = sessionmaker(bind=engine)
session = Session()


student_router = APIRouter()

# Student endpoints
@student_router.get("/student/enrolled_course/student-overview", response_model=CourseOverview,
                    description="Get an overview of the student's course including assignments and exam marks.",
                    tags=["Student"])
def get_student_course_overview(request: StudentCourseOverviewRequest):
    course_id = request.course_id
    student_id = request.student_id
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
def get_module_details(request: StudentModuleDetailsRequest):
    course_id = request.course_id
    module_id = request.module_id
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
def get_course_details(course_id: int):
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
def enroll_student(request: StudentCourseOverviewRequest):
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
def get_enrolled_courses(student_id: int):
    enrollments = session.query(CourseEnrollment).filter(CourseEnrollment.student_id == student_id).all()
    course_ids = [enrollment.course_id for enrollment in enrollments]
    courses = session.query(Course).filter(Course.id.in_(course_ids)).all()
    return [CourseEnrolled(id=course.id, title=course.title) for course in courses]

# Instructor endpoint
# @student_router.get("/instructor/enrolled-students/{course_id}", response_model=List[StudentEnrolled],
#                     tags = ["Instructor"],
#                     description="Get the list of students enrolled in a course.")
# def get_enrolled_students(course_id: int):
#     enrollments = session.query(CourseEnrollment).filter(CourseEnrollment.course_id == course_id).all()
#     student_ids = [enrollment.student_id for enrollment in enrollments]
#     students = session.query(User).filter(User.id.in_(student_ids)).all()
    
#     return [StudentEnrolled(id=student.id, username=student.username) for student in students]

# Additional endpoints that might be useful

# @student_router.post("/instructor/create-assignment", tags=["Instructor"], description="Create an assignment for a module")
# def create_assignment(request: CreateAssignmentRequest):
#     module_id = request.module_id
#     title = request.title
#     description = request.description
#     type = request.type
#     due_date = request.due_date
#     new_assignment = Assignment(
#         module_id=module_id,
#         title=title,
#         description=description,
#         type=type,
#         due_date=due_date
#     )
#     session.add(new_assignment)
#     session.commit()
#     return {"message": "Assignment created successfully", "assignment_id": new_assignment.id}

# @student_router.post("/instructor/create-exam")
# def create_exam(course_id: int, exam_id: int):
#     # Create an exam entry for each enrolled student
#     enrollments = session.query(CourseEnrollment).filter(CourseEnrollment.course_id == course_id).all()
#     for enrollment in enrollments:
#         new_exam = Exam(
#             course_id=course_id,
#             student_id=enrollment.student_id,
#             exam_id=exam_id,
#             marks=None  # Initially, no marks
#         )
#         session.add(new_exam)
#     session.commit()
#     return {"message": "Exam created successfully for all enrolled students"}

# @student_router.put("/instructor/grade-exam")
# def grade_exam(course_id: int, student_id: int, exam_id: int, marks: float):
#     exam = session.query(Exam).filter(
#         Exam.course_id == course_id,
#         Exam.student_id == student_id,
#         Exam.exam_id == exam_id
#     ).first()
#     if not exam:
#         raise HTTPException(status_code=404, detail="Exam not found")
#     exam.marks = marks
#     session.commit()
#     return {"message": "Exam graded successfully"}

# @student_router.get("/instructor/course-progress", tags=["Instructor"], description="Get the progress of a student in a course")
# def get_course_progress(request: StudentCourseOverviewRequest):
#     course_id = request.course_id
#     student_id = request.student_id
#     # Get total number of assignments and exams
#     total_assignments = session.query(func.count(Assignment.id)).join(Module).filter(Module.course_id == course_id).scalar()
#     total_exams = session.query(func.count(Exam.id)).filter(Exam.course_id == course_id, Exam.student_id == student_id).scalar()
    
#     # Get number of completed assignments and exams
#     completed_assignments = session.query(func.count(AssignmentMarks.id)).join(Assignment).join(Module).filter(
#         Module.course_id == course_id,
#         AssignmentMarks.student_id == student_id
#     ).scalar()
#     completed_exams = session.query(func.count(Exam.id)).filter(
#         Exam.course_id == course_id,
#         Exam.student_id == student_id,
#         Exam.marks != None
#     ).scalar()
    
#     # Calculate progress percentages
#     assignment_progress = (completed_assignments / total_assignments) * 100 if total_assignments > 0 else 0
#     exam_progress = (completed_exams / total_exams) * 100 if total_exams > 0 else 0
#     overall_progress = ((completed_assignments + completed_exams) / (total_assignments + total_exams)) * 100 if (total_assignments + total_exams) > 0 else 0
    
#     return {
#         "assignment_progress": assignment_progress,
#         "exam_progress": exam_progress,
#         "overall_progress": overall_progress
#     }