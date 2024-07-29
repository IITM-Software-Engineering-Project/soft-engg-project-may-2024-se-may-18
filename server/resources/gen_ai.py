from PIL import Image
import io
from typing import List
import google.generativeai as genai
from fastapi import APIRouter, File, Form, HTTPException, Request, UploadFile
import os
import json
from constants.prompts import search_courses_prompt, explain_courses_prompt, programming_feedback_prompt
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv('GEMINI_API_KEY'))


def call_gemini(prompt, data=None, data_is_json=True):
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")

    if data:
        prompt = prompt + '\n\n' + str(data)

    response = model.generate_content([prompt])

    if data_is_json:
        jstart = response.text.index("{")
        jend = response.text.rindex("}") + 1
        return json.loads(response.text[jstart:jend])
    else:
        return {"message": response.text}


def call_gemini_vision(prompt: str, images: List[UploadFile], data=None, data_is_json=True):
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    if data:
        prompt = prompt + '\n\n' + str(data)
    pil_images = []

    for file in images:
        if file.size > 0:
            pil_image = Image.open(io.BytesIO(file.file.read()))
            pil_images.append(pil_image)

    response = model.generate_content([prompt] + pil_images)

    if data_is_json:
        try:
            jstart = response.text.index("{")
            jend = response.text.rindex("}") + 1
            return json.loads(response.text[jstart:jend])
        except Exception:
            return {"message": "Failed to parse JSON response."}
    else:
        return {"message": response.text}


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
