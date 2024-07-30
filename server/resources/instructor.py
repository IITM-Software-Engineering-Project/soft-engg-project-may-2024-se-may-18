print('instructor APis')
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
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Error uploading content")


    return {
            "message": "Content added successfully",

        }
