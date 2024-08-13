from typing import List, Optional
from fastapi import APIRouter, File, Request, UploadFile
from constants.prompts import search_courses_prompt, explain_courses_prompt, programming_feedback_prompt
from dotenv import load_dotenv
from api.gemini import call_gemini, call_gemini_vision
from fastapi import HTTPException

load_dotenv()

genai_router = APIRouter()


@genai_router.post("/ai-search-courses",
                   description="Search for courses using generative AI",
                   response_description="Response from AI in the form of a json",
                   tags=["Gen AI"],
                   )
async def gemini(request: Request):
    data = await request.json()
    if "prompt" not in data.keys():
        raise HTTPException(status_code=422, detail="Prompt is required")
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
                   tags=["Gen AI"],
                   )
async def gemini(request: Request):
    data = await request.json()
    if "prompt" not in data.keys():
        raise HTTPException(status_code=422, detail="Prompt is required")
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
                   tags=["Gen AI"],
                   )
async def gemini(request: Request):
    data = await request.json()
    if "prompt" not in data.keys():
        raise HTTPException(status_code=422, detail="Prompt is required")
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
                   tags=["Gen AI"])
async def gemini(request: Request, images: List[UploadFile] = File(...)):
    print("Hi1")
    form_data = await request.form()
    prompt = form_data.get("prompt")
    data = form_data.get("data")
    language = form_data.get("language")
    question = form_data.get("question")
    print("Hi")
    prompt = programming_feedback_prompt.format(question=question,
                                                user_prompt=prompt, programming_language=language)

    response = call_gemini_vision(prompt, images, data, data_is_json=False)
    print(response)
    return response
