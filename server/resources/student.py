from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker, Session
from database.models import AssignmentQuestion, Course, CourseEnrollment, Lecture, User, Module, Assignment, AssignmentMarks, Exam
from database.db_sql import init_db
from api.payload_schema.payloadschema import CourseOverview, AssignmentSubmission, ModuleDetails, CourseDetails, EnrollmentResponse, CourseEnrolled, StudentEnrolled, StudentCourseOverviewRequest, StudentModuleDetailsRequest
from datetime import datetime
from typing import List


def get_db():
    engine = init_db()
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


student_router = APIRouter()


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
    return [CourseEnrolled(id=course.id, title=course.title, description=course.description) for course in courses]

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


@student_router.get("/student/module-content/{module_id}", tags=["Student"],
                    description="Get the content of a module i.e lectures and assignemnts.")
def get_module_content(module_id: int, session: Session = Depends(get_db)):
    module = session.query(Module).filter(Module.id == module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    lectures = session.query(Lecture).filter(
        Lecture.module_id == module_id).all()
    assignments = session.query(Assignment).filter(
        Assignment.module_id == module_id).all()
    response = {}
    response["lectures"] = []
    response["assignments"] = []
    for lecture in lectures:
        x = {}
        x["id"] = lecture.id
        x["title"] = lecture.title
        x["module_id"] = lecture.module_id
        x["url"] = lecture.url
        x["transcript"] = lecture.transcript
        response["lectures"].append(x)
    for assignment in assignments:
        y = {}
        y["id"] = assignment.id
        y["title"] = assignment.title
        y["module_id"] = assignment.module_id
        y["description"] = assignment.description
        y["type"] = assignment.type
        y["due_date"] = assignment.due_date
        response["assignments"].append(y)
    return response


@student_router.get("/student/assignment-content/{assignment_id}", tags=["Assignment"],
                    description="Get the details of an assignment including questions and marks.")
def get_assignment_details(assignment_id: int, db: Session = Depends(get_db)):
    # Fetch the assignment details
    assignment = db.query(Assignment).filter(
        Assignment.id == assignment_id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")

    # Fetch related questions
    questions = db.query(AssignmentQuestion).filter(
        AssignmentQuestion.assignment_id == assignment_id).all()

    # Fetch related marks
    marks = db.query(AssignmentMarks).filter(
        AssignmentMarks.assignment_id == assignment_id).all()

    return {
        "assignment": {
            "id": assignment.id,
            "title": assignment.title,
            "description": assignment.description,
            "type": assignment.type,
            "due_date": assignment.due_date,
        },
        "questions": [
            {
                "id": q.id,
                "question": q.question,
                "image": q.image,
                "answer_choices": q.answer_choices,
                "answer": q.answer
            }
            for q in questions
        ],
        "marks": [
            {
                "id": m.id,
                "student_id": m.student_id,
                "marks": m.marks,
                "submitted_at": m.submitted_at,
                "graded_at": m.graded_at,
                "feedback": m.feedback
            }
            for m in marks
        ]
    }


@student_router.post("/assignment/submit/{assignment_id}", tags=["Assignment"],
                     description="Submit an assignment and get scored based on correct answers.")
def submit_assignment(assignment_id: int, submission: AssignmentSubmission, db: Session = Depends(get_db)):
    # Check if the assignment exists
    assignment = db.query(Assignment).filter(
        Assignment.id == assignment_id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")

    # Fetch the assignment questions
    questions = db.query(AssignmentQuestion).filter(
        AssignmentQuestion.assignment_id == assignment_id).all()
    if not questions:
        raise HTTPException(
            status_code=404, detail="No questions found for this assignment")

    # Score the submission
    correct_answers = 0
    for question in questions:
        submitted_answer = submission.answers.get(question.id)
        if submitted_answer == question.answer:
            correct_answers += 1

    # Calculate the score (marks)
    total_questions = len(questions)
    score = (correct_answers / total_questions) * 100

    # Save the marks in AssignmentMarks
    assignment_marks = AssignmentMarks(
        assignment_id=assignment_id,
        student_id=submission.student_id,
        assignment_answer=submission.assignment_answer,
        marks=score,
        submitted_at=datetime.now(),
        graded_at=datetime.now(),
        feedback=f"You answered {correct_answers} out of {
            total_questions} correctly."
    )
    db.add(assignment_marks)
    db.commit()

    return {
        "message": "Assignment submitted successfully.",
        "score": score,
        "correct_answers": correct_answers,
        "total_questions": total_questions
    }
