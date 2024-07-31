
import google.generativeai as genai
from PIL import Image
import json
import os
from fastapi import UploadFile
from typing import List


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
