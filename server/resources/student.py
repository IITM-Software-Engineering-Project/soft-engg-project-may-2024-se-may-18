from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker, Session
from database.models import AssignmentQuestion, Course, CourseEnrollment, Lecture, User, Module, Assignment, AssignmentMarks, Exam
from database.db_sql import init_db
from api.payload_schema.payloadschema import AssignmentDetails, AssignmentQuestionDetails, CourseOverview, LectureDetails, ModuleContentDetails, ModuleDetails, CourseDetails, EnrollmentResponse, CourseEnrolled, StudentEnrolled, StudentCourseOverviewRequest, StudentModuleDetailsRequest
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

    assignments = session.query(Assignment).join(
        Module).filter(Module.course_id == course_id).all()
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


@student_router.get("/student/module-details", response_model=ModuleDetails,
                    tags=["Student"],
                    description="Get details of a module of the course.")
def get_module_details(course_id: int, module_id: int,  session: Session = Depends(get_db)):
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
                    tags=["Student"],
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
                     tags=["Student"],
                     description="Enroll a student in a course.")
def enroll_student(request: StudentCourseOverviewRequest,  session: Session = Depends(get_db)):
    student_id = request.student_id
    course_id = request.course_id
    user = session.query(User).filter(User.id == student_id).first()
    course = session.query(Course).filter(Course.id == course_id).first()
    if user is None or course is None:
        raise HTTPException(
            status_code=404, detail="Student or Course not found")
    enrollment = CourseEnrollment(
        student_id=student_id,
        course_id=course_id,
        enrollment_date=datetime.now()
    )
    if session.query(CourseEnrollment).filter(CourseEnrollment.student_id == student_id,
                                              CourseEnrollment.course_id == course_id).first():
        raise HTTPException(
            status_code=400, detail="Student is already enrolled in the course")
    session.add(enrollment)
    session.commit()
    return EnrollmentResponse(message="Enrollment successful")


@student_router.get("/student/enrolled-courses/{student_id}", response_model=List[CourseEnrolled],
                    tags=["Student"],
                    description="Get the list of courses enrolled by a student.")
def get_enrolled_courses(student_id: int, session: Session = Depends(get_db)):
    enrollments = session.query(CourseEnrollment).filter(
        CourseEnrollment.student_id == student_id).all()
    course_ids = [enrollment.course_id for enrollment in enrollments]
    courses = session.query(Course).filter(Course.id.in_(course_ids)).all()
    return [CourseEnrolled(id=course.id, title=course.title) for course in courses]

# enpoinrt to return modules in a course


@student_router.get("/student/modules/{course_id}", response_model=List[ModuleDetails],
                    tags=["Student"],
                    description="Get the list of modules in a course.")
def get_modules(course_id: int, session: Session = Depends(get_db)):
    modules = session.query(Module).filter(Module.course_id == course_id).all()
    return [ModuleDetails(
        id=module.id,
        title=module.title,
        description=module.description,
        total_lectures=module.total_lectures,
        total_assignments=module.total_assignments
    ) for module in modules]


# @student_router.get("/student/module-content/{module_id}", response_model=ModuleContentDetails,
#                     tags=["Student"],
#                     description="Get lectures, assignments, and their questions for a module.")
# def get_module_content(module_id: int, session: Session = Depends(get_db)):
#     # Fetch lectures for the module
#     lectures = session.query(Lecture).filter(
#         Lecture.module_id == module_id).all()
#     lecture_details = [
#         LectureDetails(
#             title=lecture.title,
#             url=lecture.url,
#             transcript=lecture.transcript
#         ) for lecture in lectures
#     ]
#     print(lecture_details)

#     assignments = session.query(Assignment).filter(
#         Assignment.module_id == module_id).all()
#     assignment_details = []

#     print(assignments)

#     for assignment in assignments:
#         questions = session.query(AssignmentQuestion).filter(
#             AssignmentQuestion.assignment_id == assignment.id).all()

#         question_details = [
#             AssignmentQuestionDetails(
#                 question=question.question,
#                 answer_choices=question.answer_choices,
#                 answer=question.answer,
#                 image=question.image
#             ) for question in questions
#         ]
#         assignment_details.append(
#             AssignmentDetails(
#                 title=assignment.title,
#                 description=assignment.description,
#                 type=assignment.type,
#                 due_date=assignment.due_date.isoformat(),
#                 questions=question_details
#             )
#         )

#     return ModuleContentDetails(
#         lectures=lecture_details,
#         assignments=assignment_details
#     )

@student_router.get("/student/module-content/{module_id}", tags=["Student"], 
                    description="Get the content of a module i.e lectures and assignemnts.")
def get_module_content(module_id: int, session: Session = Depends(get_db)):
    module = session.query(Module).filter(Module.id == module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    lectures = session.query(Lecture).filter(Lecture.module_id == module_id).all()
    assignments = session.query(Assignment).filter(Assignment.module_id == module_id).all()
    response = {}
    response["lectures"] = []
    response["assignments"] = []
    for lecture in lectures:
        x={}
        x["id"] = lecture.id
        x["title"] = lecture.title
        x["module_id"] = lecture.module_id
        x["url"] = lecture.url
        x["transcript"] = lecture.transcript
        response["lectures"].append(x) 
    for assignment in assignments:
        y={}
        y["id"]=assignment.id
        y["title"]=assignment.title
        y["module_id"]=assignment.module_id
        y["description"]=assignment.description
        y["type"]=assignment.type
        y["due_date"]=assignment.due_date
        response["assignments"].append(y)
    return response


@student_router.get("/student/course-content/{course_id}", tags=["Student"],
                        description="Get the content of a course i.e modules, lectures and assignemnts.")
def get_course_content(course_id: int, session: Session = Depends(get_db)):
    modules = session.query(Module).filter(Module.course_id == course_id).all()
    response = {}
    response["modules"] = []
    for module in modules:
        x={}
        x["id"] = module.id
        x["title"] = module.title
        x["total_lectures"] = module.total_lectures
        x["total_assignments"] = module.total_assignments
        x["description"] = module.description
        x["lectures"] = []
        x["assignments"] = []
        lectures = session.query(Lecture).filter(Lecture.module_id == module.id).all()
        assignments = session.query(Assignment).filter(Assignment.module_id == module.id).all()
        for lecture in lectures:
            y={}
            y["id"] = lecture.id
            y["title"] = lecture.title
            y["module_id"] = lecture.module_id
            y["url"] = lecture.url
            y["transcript"] = lecture.transcript
            x["lectures"].append(y) 
        for assignment in assignments:
            y={}
            y["id"]=assignment.id
            y["title"]=assignment.title
            y["module_id"]=assignment.module_id
            y["description"]=assignment.description
            y["type"]=assignment.type
            y["due_date"]=assignment.due_date
            x["assignments"].append(y)

        response["modules"].append(x)
    return response

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
