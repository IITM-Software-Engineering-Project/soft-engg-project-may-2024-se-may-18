from sqlite3 import IntegrityError
from fastapi import APIRouter, HTTPException, Request
from database.models import Content, session

instructor_router= APIRouter()


@instructor_router.post('/add_content')
async def add_content(request: Request):
    data= await request.json()
    content=Content(**data)

    try:
        with session.begin() as db:
            db.add(content)
            db.commit()
            db.close()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error uploading content:{e}")


    return {
            "message": "Content added successfully",

        }
@instructor_router.put('/edit_content/{content_id}')
async def edit_content(content_id: int):
    data = await request.json()

    content = db.query(Content).filter(Content.id == content_id).first()
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")

    for key, value in data.items():
        setattr(content, key, value)

    try:
        db.commit()
        db.refresh(content)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error updating content")

    return {
        "message": "Content updated successfully",
        "content": content
    }


@instructor_router.delete('/delete_content/{content_id}')
async def delete_content(content_id: int):
    content = db.query(Content).filter(Content.id == content_id).first()
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")

    try:
        db.delete(content)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error deleting content")

    return {
        "message": "Content deleted successfully"
    }