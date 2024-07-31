from sqlite3 import IntegrityError
from fastapi import APIRouter, HTTPException, Request
from database.models import Module, session, Course,Lecture, Assignment

instructor_router= APIRouter()




'''Add, Edit, Delete Modules'''
@instructor_router.post('/add_module',
                  description="Add new module to course",
                  response_description="Message indicating success or failure",
                  tags=["Instructor", "Module"])
async def add_module(request: Request):
    data= await request.json()
    module=Module(**data)

    try:
        with session.begin() as db:
            db.add(module)
            db.commit()
            db.close()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error uploading Module:{e}")


    return {
            "message": "Module added successfully",

        }
@instructor_router.put('/edit_module/{module_id}',
                  description="Editing new module",
                  response_description="Message indicating success or failure",
                  tags=["Instructor", "Module"])
async def edit_module(module_id: int):
    data = await request.json()

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
    data= await request.json()
    lecture=Lecture(**data)

    try:
        with session.begin() as db:
            db.add(lecture)
            db.commit()
            db.close()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error uploading lecture:{e}")


    return {
            "message": "Lecture added successfully",

        }
@instructor_router.put('/edit_lecture/{lecture_id}',
                  description="Editing lecture",
                  response_description="Message indicating success or failure",
                  tags=["Instructor", "Lecture"])
async def edit_lecture(lecture_id: int):
    data = await request.json()

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
    data= await request.json()
    assignment=Assignment(**data)

    try:
        with session.begin() as db:
            db.add(assignment)
            db.commit()
            db.close()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error uploading assignment:{e}")


    return {
            "message": "assignment added successfully",

        }
@instructor_router.put('/edit_assignment/{assignment_id}',
                  description="Editing Assignment",
                  response_description="Message indicating success or failure",
                  tags=["Module", "Assignment","Instructor"])
async def edit_assignment(assignment_id: int):
    data = await request.json()

    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="assignment not found")

    for key, value in data.items():
        setattr(assignment, key, value)

    try:

        db.commit()
        db.refresh(assignment)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error updating assignment")

    return {
        "message": "assignment updated successfully",
        
    }


@instructor_router.delete('/delete_assignment/{assignment_id}',
                  description="Deleting Assignment",
                  response_description="Message indicating success or failure",
                  tags=["Assignment", "Module"])
async def delete_assignment(assignment_id: int):
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="lecture not found")

    try:
        db.delete(assignment)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error deleting assignment")

    return {
        "message": "assignment deleted successfully"
    }









'''Add, Edit, Delete Questions'''

@instructor_router.post('/add_question',
                  description="Adding question to assignment",
                  response_description="Message indicating success or failure",
                  tags=["Assignment", "Module"])
async def add_question(request: Request):
    data= await request.json()
    question=AssignmentQuestion(**data)

    try:
        with session.begin() as db:
            db.add(question)
            db.commit()
            db.close()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error uploading question:{e}")


    return {
            "message": "Question added successfully",

        }
@instructor_router.put('/edit_question/{question_id}' ,
                  description="Edit Question ",
                  response_description="Message indicating success or failure",
                  tags=["Question", "Assignment"])
async def edit_question(question_id: int):
    data = await request.json()

    question = db.query(AssignmentQuestion).filter(AssignmentQuestion.id == question_id).first()
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
async def delete_question(aquestion_id: int):
    question = db.query(AssignmentQuestion).filter(AssignmentQuestion.id == question_id).first()
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
