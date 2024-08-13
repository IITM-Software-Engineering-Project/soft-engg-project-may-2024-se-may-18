from sqlite3 import IntegrityError
from typing import List
from fastapi import APIRouter, HTTPException, Request, Depends
from sqlalchemy import func
from database.models import AssignmentMarks, AssignmentQuestion, CourseEnrollment, Exam, Module, User, session, Course, Lecture, Assignment
from api.payload_schema.payloadschema import CreateAssignmentRequest, StudentCourseOverviewRequest, StudentEnrolled
from database.db_sql import init_db
from sqlalchemy.orm import sessionmaker, Session
from database.models import Module, Lecture, Assignment, AssignmentQuestion, CourseEnrollment, Exam, User
from datetime import datetime
instructor_router = APIRouter()

def get_db():
    engine = init_db()
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


'''Add, Edit, Delete Modules'''


@instructor_router.post('/add_module',
                        description="Add new module to course",
                        response_description="Message indicating success or failure",
                        tags=["Module"])
async def add_module(request: Request, session: Session = Depends(get_db)):
    data = await request.json()
    module = Module(**data)
    if(not session.query(Course).filter(Course.id == module.course_id).first()):
        raise HTTPException(status_code=404, detail="Course not found")

    try:
        session.add(module)
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=400, detail=f"Error uploading Module: {e}")

    return {
        "message": "Module added successfully",
    }


@instructor_router.put('/edit_module/{module_id}',
                       description="Editing new module",
                       response_description="Message indicating success or failure",
                       tags=["Module"])
async def edit_module(request: Request, module_id: int, session: Session = Depends(get_db)):
    data = await request.json()

    module = session.query(Module).filter(Module.id == module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="Content not found")

    for key, value in data.items():
        setattr(module, key, value)

    try:
        session.commit()
        session.refresh(module)
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="Error updating Module")

    return {
        "message": "Module updated successfully",

    }


@instructor_router.delete('/delete_module/{module_id}',
                          description="Delete module",
                          response_description="Message indicating success or failure",
                          tags=["Module"])
async def delete_module(module_id: int, session: Session = Depends(get_db)):
    module = session.query(Module).filter(Module.id == module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")

    try:
        session.delete(module)
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="Error deleting Module")

    return {
        "message": "Module deleted successfully"
    }


'''Add, Edit, Delete Lectures'''


@instructor_router.post('/add_lecture',
                        description="Add lecture to a module",
                        response_description="Message indicating success or failure",
                        tags=["Lecture"])
async def add_lecture(request: Request, session: Session = Depends(get_db)):
    data = await request.json()
    lecture = Lecture(**data)
    if(not session.query(Module).filter(Module.id == lecture.module_id).first()):
        raise HTTPException(status_code=404, detail="Module not found")
    try:
        session.add(lecture)
        session.commit()
        session.close()
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error uploading lecture:{e}")

    return {
        "message": "Lecture added successfully",

    }


@instructor_router.put('/edit_lecture/{lecture_id}',
                       description="Editing lecture",
                       response_description="Message indicating success or failure",
                       tags=["Lecture"])
async def edit_lecture(request: Request, lecture_id: int, session: Session = Depends(get_db)):
    data = await request.json()
    lecture = session.query(Lecture).filter(Lecture.id == lecture_id).first()
    if not lecture:
        raise HTTPException(status_code=404, detail="lecture not found")

    for key, value in data.items():
        setattr(lecture, key, value)

    try:
        session.commit()
        session.refresh(lecture)
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="Error updating lecture")

    return {
        "message": "lecture updated successfully",
    }


@instructor_router.delete('/delete_lecture/{lecture_id}',
                          description="Deleting Lecture from the module",
                          response_description="Message indicating success or failure",
                          tags=["Lecture"])
async def delete_lecture(lecture_id: int, session: Session = Depends(get_db)):
    lecture = session.query(Lecture).filter(Lecture.id == lecture_id).first()
    if not lecture:
        raise HTTPException(status_code=404, detail="lecture not found")

    try:
        session.delete(lecture)
        session.commit()

    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="Error deleting lecture")

    return {
        "message": "lecture deleted successfully"
    }


'''Add, Edit, Delete Assignments'''


@instructor_router.post('/add_assignment',
                        description="Adding assignment to module",
                        response_description="Message indicating success or failure",
                        tags=["Assignment", "Module"])
async def add_assignment(request: Request, session: Session = Depends(get_db)):
    data = await request.json()
    data['due_date'] = datetime.strptime(data['due_date'], "%Y-%m-%d %H:%M:%S")
    assignment = Assignment(**data)
    
    if(not session.query(Module).filter(Module.id == assignment.module_id).first()):
        raise HTTPException(status_code=404, detail="Module not found")
    try:
        session.add(assignment)
        session.commit()
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error uploading assignment:{e}")

    return {
        "message": "assignment added successfully",

    }


@instructor_router.put('/edit_assignment/{assignment_id}',
                       description="Editing Assignment",
                       response_description="Message indicating success or failure",
                       tags=["Module", "Assignment"])
async def edit_assignment(request: Request, assignment_id: int, session: Session = Depends(get_db)):
    data = await request.json()
    assignment = session.query(Assignment).filter(Assignment.id == assignment_id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="assignment not found")
    if "module_id" in data.keys() and session.query(Module).filter_by(id = data["module_id"]).first() is None:
        raise HTTPException(status_code=404, detail="Module not found")

    for key, value in data.items():
        setattr(assignment, key, value)

    try:
        session.commit()
        session.refresh(assignment)
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=400, detail="Error updating assignment")

    return {
        "message": "assignment updated successfully",

    }


@instructor_router.delete('/delete_assignment/{assignment_id}',
                          description="Deleting Assignment",
                          response_description="Message indicating success or failure",
                          tags=["Assignment", "Module"])
async def delete_assignment(assignment_id: int, session: Session = Depends(get_db)):
    assignment = session.query(Assignment).filter(Assignment.id == assignment_id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="assignment not found")
    
    try:
        session.delete(assignment)
        session.commit()
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=400, detail=f"Error deleting assignment : {e}")

    return {
        "message": "assignment deleted successfully"
    }


'''Add, Edit, Delete Questions'''


@instructor_router.post('/add_question',
                        description="Adding question to assignment",
                        response_description="Message indicating success or failure",
                        tags=["Assignment"])
async def add_question(request: Request, session: Session = Depends(get_db)):
    data = await request.json()
    question = AssignmentQuestion(**data)
    if("options" not in data.keys()):
        raise HTTPException(status_code=400, detail=f"Missing fields in payload")
    if ("answer" not in data.keys()):
        raise HTTPException(status_code=400, detail=f"Missing fields in payload")
    if ("assignment_id" not in data.keys()):
        raise HTTPException(status_code=400, detail=f"Missing fields in payload")
    
    
    try:
        session.add(question)
        session.commit()
        session.close()
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error uploading question:{e}")

    return {
        "message": "Question added successfully",

    }


@instructor_router.put('/edit_question/{question_id}',
                       description="Edit Question ",
                       response_description="Message indicating success or failure",
                       tags=["Assignment"])
async def edit_question(request: Request, question_id: int, session: Session = Depends(get_db)):
    data = await request.json()
    if(len(data)<1):
        raise HTTPException(status_code = 422, detail="missing fields")
    question = session.query(AssignmentQuestion).filter(AssignmentQuestion.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="question not found")

    for key, value in data.items():
        setattr(question, key, value)

    try:
        session.commit()
        session.refresh(question)
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="Error updating question")

    return {
        "message": "question updated successfully",

    }


@instructor_router.delete('/delete_question/{question_id}',
                          description="Delete question from Assignment",
                          response_description="Message indicating success or failure",
                          tags=["Assignment"])
async def delete_question(question_id: int, session: Session = Depends(get_db)):
    question = session.query(AssignmentQuestion).filter(AssignmentQuestion.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="question not found")

    try:
        session.delete(question)
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="Error deleting question")

    return {
        "message": "question deleted successfully"
    }


@instructor_router.get("/instructor/enrolled-students/{course_id}", response_model=List[StudentEnrolled],
                       tags=["Instructor","Admin"],
                       description="Get the list of students enrolled in a course.")
def get_enrolled_students(course_id: int, session: Session = Depends(get_db)):
    enrollments = session.query(CourseEnrollment).filter(
        CourseEnrollment.course_id == course_id).all()
    student_ids = [enrollment.student_id for enrollment in enrollments]
    students = session.query(User).filter(User.id.in_(student_ids)).all()

    return [StudentEnrolled(id=student.id, username=student.username) for student in students]


@instructor_router.post("/instructor/create-exam", tags=["Exam"], description="Create an exam for a course")
def create_exam(course_id: int, exam_id: int, session: Session = Depends(get_db)):
    # Create an exam entry for each enrolled student
    if(session.query(Course).filter_by(id=course_id).first() is None):
        raise HTTPException(status_code=404, detail="course not found")
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


@instructor_router.put("/instructor/grade-exam", tags=["Exam"], description="Grade an exam")
def grade_exam(course_id: int, student_id: int, exam_id: int, marks: float, session: Session = Depends(get_db)):
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


@instructor_router.get("/course-progress", tags=["Instructor"], description="Get the progress of a student in a course")
def get_course_progress(course_id: int, student_id: int, session: Session = Depends(get_db)):
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
