from sqlite3 import IntegrityError
from fastapi import APIRouter, HTTPException, Request
from database.models import Module, session, Course,Lecture, Assignment

instructor_router= APIRouter()




'''Add, Edit, Delete Modules'''
@instructor_router.post('/add_module')
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
@instructor_router.put('/edit_module/{module_id}')
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


@instructor_router.delete('/delete_module/{module_id}')
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

@instructor_router.post('/add_lecture')
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
@instructor_router.put('/edit_lecture/{lecture_id}')
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


@instructor_router.delete('/delete_lecture/{lecture_id}')
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

@instructor_router.post('/add_assignment')
async def add_lecture(request: Request):
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
@instructor_router.put('/edit_assignment/{assignment_id}')
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


@instructor_router.delete('/delete_assignment/{assignment_id}')
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