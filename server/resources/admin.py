from fastapi import HTTPException, APIRouter
from typing import List
from sqlalchemy.orm import sessionmaker
from database.db_sql import init_db
from api.payload_schema.payloadschema import CourseCreate, CourseUpdate, CourseResponse
from database.models import Course  # Import the SQLAlchemy Course model
engine = init_db()
admin_router = APIRouter()
Session = sessionmaker(bind=engine)
db = Session()


@admin_router.post("/courses/create", response_model=CourseResponse, tags=["Admin"], description="Create a new course")
async def create_course(course: CourseCreate):
    db_course = Course(**course.model_dump())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

@admin_router.put("/courses/update", response_model=CourseResponse, tags=["Admin"], description="Update a course")
async def update_course(course: CourseUpdate):
    db_course = db.query(Course).filter(Course.id == course.id).first()
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    for key, value in course.model_dump(exclude={'id'}).items():
        setattr(db_course, key, value)
    
    db.commit()
    db.refresh(db_course)
    return db_course

@admin_router.delete("/courses/delete", response_model=dict, tags=["Admin"], description="Delete a course")
async def delete_course(id:int):
    db_course = db.query(Course).filter(Course.id == id).first()
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    db.delete(db_course)
    db.commit()
    return {"message": "Course deleted successfully"}

@admin_router.get("/courses/get", response_model=CourseResponse, tags=["Admin"], description="Get a course by ID")
async def get_course(id:int):
    db_course = db.query(Course).filter(Course.id == id).first()
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")
    return db_course

@admin_router.get("/courses/list", response_model=List[CourseResponse], tags=["Admin"], description="Get all courses with pagination")
async def get_all_courses(limit: int = 100, skip: int = 0):
    courses = db.query(Course).offset(skip).limit(limit).all()
    return courses