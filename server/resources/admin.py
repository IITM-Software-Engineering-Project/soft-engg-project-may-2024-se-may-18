from fastapi import HTTPException, APIRouter, Depends, Request
from typing import List
from sqlalchemy.orm import sessionmaker, Session
from database.db_sql import init_db
from api.payload_schema.payloadschema import CourseCreate, CourseUpdate, CourseResponse
from database.models import Course  # Import the SQLAlchemy Course model

admin_router = APIRouter()
def get_db():
    engine = init_db()
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@admin_router.post("/courses/create", response_model=CourseResponse, tags=["Admin"], description="Create a new course")
async def create_course(course: CourseCreate, session: Session = Depends(get_db)):
    db_course = Course(**course.model_dump())
    session.add(db_course)
    session.commit()
    # session.refresh(db_course)
    return db_course

@admin_router.put("/courses/update", response_model=CourseResponse, tags=["Admin"], description="Update a course")
async def update_course(request:Request, session: Session = Depends(get_db)):
    data = await request.json()
    course_id = int(data.get('id'))
    db_course = session.query(Course).filter(Course.id == course_id).first()
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    
    for key, value in data.items():
        setattr(db_course, key, value)
    
    session.commit()
    session.refresh(db_course)
    return db_course

@admin_router.delete("/courses/delete", response_model=dict, tags=["Admin"], description="Delete a course")
async def delete_course(id:int, session: Session = Depends(get_db)):
    db_course = session.query(Course).filter(Course.id == id).first()
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    session.delete(db_course)
    session.commit()
    return {"message": "Course deleted successfully"}

@admin_router.get("/courses/get", response_model=CourseResponse, tags=["Admin"], description="Get a course by ID")
async def get_course(id:int, session: Session = Depends(get_db)):
    db_course = session.query(Course).filter(Course.id == id).first()
    print(db_course)
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")
    return db_course

@admin_router.get("/courses/list", response_model=List[CourseResponse], tags=["Admin"], description="Get all courses with pagination")
async def get_all_courses(limit: int = 100, skip: int = 0, session: Session = Depends(get_db)):
    courses = session.query(Course).offset(skip).limit(limit).all()
    return courses