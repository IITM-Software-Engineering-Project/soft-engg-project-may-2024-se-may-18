from sqlite3 import IntegrityError
from typing import List
from fastapi import APIRouter, HTTPException, Request
from sqlalchemy import func
from database.models import AssignmentMarks, AssignmentQuestion, CourseEnrollment, Exam, Module, User, session, Course, Lecture, Assignment
from server.api.payload_schema.payloadschema import CreateAssignmentRequest, StudentCourseOverviewRequest, StudentEnrolled

instructor_router = APIRouter()


'''Add, Edit, Delete Modules'''


@instructor_router.post('/add_module',
                        description="Add new module to course",
                        response_description="Message indicating success or failure",
                        tags=["Instructor", "Module"])
async def add_module(request: Request):
    data = await request.json()
    module = Module(**data)

    try:
        with session.begin() as db:
            db.add(module)
            db.commit()
            db.close()
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error uploading Module:{e}")

    return {
        "message": "Module added successfully",

    }


@instructor_router.put('/edit_module/{module_id}',
                       description="Editing new module",
                       response_description="Message indicating success or failure",
                       tags=["Instructor", "Module"])
async def edit_module(request: Request, module_id: int):
    data = await request.json()

    with session.begin() as db:
        module = db.query(Module).filter(Module.id == module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="Content not found")

    for key, value in data.items():
        setattr(module, key, value)

    try:
        db.commit()
        db.refresh(module)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error updating Module")

    return {
        "message": "Module updated successfully",

    }


@instructor_router.delete('/delete_module/{module_id}',
                          description="Delete module",
                          response_description="Message indicating success or failure",
                          tags=["Instructor", "Module"])
async def delete_module(module_id: int):
    with session.begin() as db:
        module = db.query(Module).filter(Module.id == module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")

    try:
        db.delete(module)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error deleting Module")

    return {
        "message": "Module deleted successfully"
    }


'''Add, Edit, Delete Lectures'''


@instructor_router.post('/add_lecture',
                        description="Add lecture to a module",
                        response_description="Message indicating success or failure",
                        tags=["Instructor", "Lecture"])
async def add_lecture(request: Request):
    data = await request.json()
    lecture = Lecture(**data)

    try:
        with session.begin() as db:
            db.add(lecture)
            db.commit()
            db.close()
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error uploading lecture:{e}")

    return {
        "message": "Lecture added successfully",

    }


@instructor_router.put('/edit_lecture/{lecture_id}',
                       description="Editing lecture",
                       response_description="Message indicating success or failure",
                       tags=["Instructor", "Lecture"])
async def edit_lecture(request: Request, lecture_id: int):
    data = await request.json()
    with session.begin() as db:
        lecture = db.query(Lecture).filter(Lecture.id == lecture_id).first()
    if not lecture:
        raise HTTPException(status_code=404, detail="lecture not found")

    for key, value in data.items():
        setattr(lecture, key, value)

    try:
        db.commit()
        db.refresh(lecture)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error updating lecture")

    return {
        "message": "lecture updated successfully",

    }


@instructor_router.delete('/delete_lecture/{lecture_id}',
                          description="Deleting Lecture from the module",
                          response_description="Message indicating success or failure",
                          tags=["Instructor", "Lecture"])
async def delete_lecture(lecture_id: int):
    with session.begin() as db:
        lecture = db.query(Lecture).filter(Lecture.id == lecture_id).first()
    if not lecture:
        raise HTTPException(status_code=404, detail="lecture not found")

    try:
        db.delete(lecture)
        db.commit()

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error deleting lecture")

    return {
        "message": "lecture deleted successfully"
    }


'''Add, Edit, Delete Assignments'''


@instructor_router.post('/add_assignment',
                        description="Adding assignment to module",
                        response_description="Message indicating success or failure",
                        tags=["Assignnment", "Module"])
async def add_assignment(request: Request):
    data = await request.json()
    assignment = Assignment(**data)

    try:
        with session.begin() as db:
            db.add(assignment)
            db.commit()
            db.close()
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error uploading assignment:{e}")

    return {
        "message": "assignment added successfully",

    }


@instructor_router.put('/edit_assignment/{assignment_id}',
                       description="Editing Assignment",
                       response_description="Message indicating success or failure",
                       tags=["Module", "Assignment", "Instructor"])
async def edit_assignment(request: Request, assignment_id: int):
    data = await request.json()
    with session.begin() as db:
        assignment = db.query(Assignment).filter(
            Assignment.id == assignment_id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="assignment not found")

    for key, value in data.items():
        setattr(assignment, key, value)

    try:

        db.commit()
        db.refresh(assignment)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400, detail="Error updating assignment")

    return {
        "message": "assignment updated successfully",

    }


@instructor_router.delete('/delete_assignment/{assignment_id}',
                          description="Deleting Assignment",
                          response_description="Message indicating success or failure",
                          tags=["Assignment", "Module"])
async def delete_assignment(assignment_id: int):
    with session.begin() as db:
        assignment = db.query(Assignment).filter(
            Assignment.id == assignment_id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="lecture not found")

    try:
        db.delete(assignment)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400, detail="Error deleting assignment")

    return {
        "message": "assignment deleted successfully"
    }


'''Add, Edit, Delete Questions'''


@instructor_router.post('/add_question',
                        description="Adding question to assignment",
                        response_description="Message indicating success or failure",
                        tags=["Assignment", "Module"])
async def add_question(request: Request):
    data = await request.json()
    question = AssignmentQuestion(**data)

    try:
        with session.begin() as db:
            db.add(question)
            db.commit()
            db.close()
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error uploading question:{e}")

    return {
        "message": "Question added successfully",

    }


@instructor_router.put('/edit_question/{question_id}',
                       description="Edit Question ",
                       response_description="Message indicating success or failure",
                       tags=["Question", "Assignment"])
async def edit_question(request: Request, question_id: int):
    data = await request.json()
    with session.begin() as db:
        question = db.query(AssignmentQuestion).filter(
            AssignmentQuestion.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="question not found")

    for key, value in data.items():
        setattr(question, key, value)

    try:

        db.commit()
        db.refresh(question)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error updating question")

    return {
        "message": "question updated successfully",

    }


@instructor_router.delete('/delete_question/{question_id}',
                          description="Delete question from Assignment",
                          response_description="Message indicating success or failure",
                          tags=["Question", "Assignment"])
async def delete_question(question_id: int):
    with session.begin() as db:
        question = db.query(AssignmentQuestion).filter(
            AssignmentQuestion.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="question not found")

    try:
        db.delete(question)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error deleting question")

    return {
        "message": "question deleted successfully"
    }


@instructor_router.get("/instructor/enrolled-students/{course_id}", response_model=List[StudentEnrolled],
                       tags=["Instructor"],
                       description="Get the list of students enrolled in a course.")
def get_enrolled_students(course_id: int):
    enrollments = session.query(CourseEnrollment).filter(
        CourseEnrollment.course_id == course_id).all()
    student_ids = [enrollment.student_id for enrollment in enrollments]
    students = session.query(User).filter(User.id.in_(student_ids)).all()

    return [StudentEnrolled(id=student.id, username=student.username) for student in students]


# @instructor_router.post("/instructor/create-assignment", tags=["Instructor"], description="Create an assignment for a module")
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


@instructor_router.post("/instructor/create-exam")
def create_exam(course_id: int, exam_id: int):
    # Create an exam entry for each enrolled student
    enrollments = session.query(CourseEnrollment).filter(
        CourseEnrollment.course_id == course_id).all()
    for enrollment in enrollments:
        new_exam = Exam(
            course_id=course_id,
            student_id=enrollment.student_id,
            exam_id=exam_id,
            marks=None  # Initially, no marks
        )
        session.add(new_exam)
    session.commit()
    return {"message": "Exam created successfully for all enrolled students"}


@instructor_router.put("/instructor/grade-exam")
def grade_exam(course_id: int, student_id: int, exam_id: int, marks: float):
    exam = session.query(Exam).filter(
        Exam.course_id == course_id,
        Exam.student_id == student_id,
        Exam.exam_id == exam_id
    ).first()
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    exam.marks = marks
    session.commit()
    return {"message": "Exam graded successfully"}


@instructor_router.get("/instructor/course-progress", tags=["Instructor"], description="Get the progress of a student in a course")
def get_course_progress(request: StudentCourseOverviewRequest):
    course_id = request.course_id
    student_id = request.student_id
    # Get total number of assignments and exams
    total_assignments = session.query(func.count(Assignment.id)).join(
        Module).filter(Module.course_id == course_id).scalar()
    total_exams = session.query(func.count(Exam.id)).filter(
        Exam.course_id == course_id, Exam.student_id == student_id).scalar()

    # Get number of completed assignments and exams
    completed_assignments = session.query(func.count(AssignmentMarks.id)).join(Assignment).join(Module).filter(
        Module.course_id == course_id,
        AssignmentMarks.student_id == student_id
    ).scalar()
    completed_exams = session.query(func.count(Exam.id)).filter(
        Exam.course_id == course_id,
        Exam.student_id == student_id,
        Exam.marks != None
    ).scalar()

    # Calculate progress percentages
    assignment_progress = (
        completed_assignments / total_assignments) * 100 if total_assignments > 0 else 0
    exam_progress = (completed_exams / total_exams) * \
        100 if total_exams > 0 else 0
    overall_progress = ((completed_assignments + completed_exams) / (total_assignments +
                        total_exams)) * 100 if (total_assignments + total_exams) > 0 else 0

    return {
        "assignment_progress": assignment_progress,
        "exam_progress": exam_progress,
        "overall_progress": overall_progress
    }
