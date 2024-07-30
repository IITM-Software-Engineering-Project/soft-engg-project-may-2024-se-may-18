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
