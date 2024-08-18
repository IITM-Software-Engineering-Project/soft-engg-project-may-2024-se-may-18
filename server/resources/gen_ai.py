from typing import List, Optional, Annotated
from fastapi import APIRouter, File, Request, UploadFile, Depends, Form
from constants.prompts import search_courses_prompt, explain_courses_prompt, programming_feedback_prompt, summary_transcript_prompt, textual_answer_grading_prompt
from dotenv import load_dotenv
from api.gemini import call_gemini, call_gemini_vision
from fastapi import HTTPException

from sqlalchemy.orm import sessionmaker, Session
from database.models import Course
from database.db_sql import init_db

load_dotenv()

genai_router = APIRouter()


def get_db():
    engine = init_db()
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@genai_router.post("/ai-search-courses",
                   description="Search for courses using generative AI",
                   response_description="Response from AI in the form of a json",
                   tags=["Gen AI"],
                   )
async def gemini(request: Request, session: Session = Depends(get_db)):
    data = await request.json()
    if "prompt" not in data.keys():
        raise HTTPException(status_code=422, detail="Prompt is required")
    prompt = data["prompt"]
    prompt = search_courses_prompt.format(user_prompt=prompt)
    try:
        data = data["data"]
    except Exception:
        x = session.query(Course).all()

        data = []
        for i in x:
            data.append({
                "course_id": i.id,
                "course_title": i.title,
                "course_description": i.description
            })

    response = call_gemini(prompt, data)
    return response


@genai_router.post("/ai-explain-course",
                   description="Answer queston for a single course using generative AI",
                   response_description="Response from AI in the form of a json with a text message inside",
                   tags=["Gen AI"],
                   )
async def gemini(request: Request, course_id: int, session: Session = Depends(get_db)):
    data = await request.json()
    if "prompt" not in data.keys():
        raise HTTPException(status_code=422, detail="Prompt is required")
    prompt = data["prompt"]
    prompt = explain_courses_prompt.format(user_prompt=prompt)
    try:
        data = data["data"]
    except Exception:
        course = session.query(Course).filter(Course.id == course_id).first()
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")

        data = []
        data.append({
            "course_id": course.id,
            "course_title": course.title,
            "course_description": course.description
        })

    response = call_gemini(prompt, data)
    return response


@genai_router.post("/ai-summarize-transcript",
                   description="Summarize a transcript using generative AI",
                   response_description="Response from AI in the form of a json with a text message inside",
                   tags=["Gen AI"],
                   )
async def gemini(request: Request):
    data = await request.json()
    if "prompt" not in data.keys():
        raise HTTPException(status_code=422, detail="Prompt is required")
    prompt = data["prompt"]
    prompt = summary_transcript_prompt.format(user_prompt=prompt)
    try:
        data = data["data"]
    except Exception:
        data = None

    response = call_gemini(prompt, data)
    return response


@genai_router.post("/ai-programming-feedback",
                   description="Get feedback on programming code using generative AI",
                   response_description="Response from AI in the form of a JSON with a text message inside",
                   tags=["Gen AI"])
async def gemini(prompt: Annotated[str, Form()], data: Annotated[str, Form()], language: Annotated[str, Form()], question: Annotated[str, Form()]):
    prompt = programming_feedback_prompt.format(question=question,
                                                user_prompt=prompt, programming_language=language)

    response = call_gemini(prompt, data, data_is_json=True)
    print(response)
    return response


@genai_router.post("/grade-text-question",
                   description="Grade a textual answer based on the question using generative AI",
                   response_description="Response from AI in the form of a JSON with score and description",
                   tags=["Grading AI"])
async def grade_text_question(request: Request):
    data = await request.json()

    if "question" not in data.keys() or "answer" not in data.keys():
        raise HTTPException(
            status_code=422, detail="Both 'question' and 'answer' are required")

    question = data["question"]
    answer = data["answer"]

    # Format the prompt with the question and answer
    prompt = textual_answer_grading_prompt.format(
        question=question, answer=answer)

    # Call the generative AI to grade the answer
    response = call_gemini(prompt)

    return response
