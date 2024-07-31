from typing import List
from fastapi import APIRouter, File, Request, UploadFile
from constants.prompts import search_courses_prompt, explain_courses_prompt, programming_feedback_prompt
from dotenv import load_dotenv
from api.gemini import call_gemini, call_gemini_vision

load_dotenv()

genai_router = APIRouter()


@genai_router.post("/ai-search-courses",
                   description="Search for courses using generative AI",
                   response_description="Response from AI in the form of a json",
                   tags=["Gen AI", "Search Courses"],
                   )
async def gemini(request: Request):
    data = await request.json()
    prompt = data["prompt"]
    prompt = search_courses_prompt.format(user_prompt=prompt)
    try:
        data = data["data"]
    except Exception:
        data = None

    response = call_gemini(prompt, data)
    return response


@genai_router.post("/ai-explain-course",
                   description="Answer queston for a single course using generative AI",
                   response_description="Response from AI in the form of a json with a text message inside",
                   tags=["Gen AI", "Explain Courses"],
                   )
async def gemini(request: Request):
    data = await request.json()
    prompt = data["prompt"]
    prompt = explain_courses_prompt.format(user_prompt=prompt)
    try:
        data = data["data"]
    except Exception:
        data = None

    response = call_gemini(prompt, data)
    return response


@genai_router.post("/ai-summarize-transcript",
                   description="Summarize a transcript using generative AI",
                   response_description="Response from AI in the form of a json with a text message inside",
                   tags=["Gen AI", "Summarize Transcript"],
                   )
async def gemini(request: Request):
    data = await request.json()
    prompt = data["prompt"]
    try:
        data = data["data"]
    except Exception:
        data = None

    response = call_gemini(prompt, data, data_is_json=False)
    return response


@genai_router.post("/ai-programming-feedback",
                   description="Get feedback on programming code using generative AI",
                   response_description="Response from AI in the form of a JSON with a text message inside",
                   tags=["Gen AI", "Programming Feedback"])
async def gemini(request: Request, images: List[UploadFile] = File(...)):
    form_data = await request.form()
    prompt = form_data.get("prompt")
    data = form_data.get("data")
    language = form_data.get("language")
    question = form_data.get("question")
    prompt = programming_feedback_prompt.format(question=question,
                                                user_prompt=prompt, programming_language=language)

    response = call_gemini_vision(prompt, images, data, data_is_json=False)

    return response
