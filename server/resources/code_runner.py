from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
import requests

code_runner_router = APIRouter()

# Replace these with your JDoodle credentials
CLIENT_ID = "d5074dbfe7c2103094a5e1f672956a19"
CLIENT_SECRET = "d0b13c44223cda1e0a6e97d8c7bea5f581d6c46de7a6820e0a3e28537ebcc839"


class CodeExecutionRequest(BaseModel):
    code: str
    language: str
    versionIndex: str


@code_runner_router.post("/execute-code")
async def execute_code(request: Request):
    data = await request.json()
    execution_data = {
        "clientId": CLIENT_ID,
        "clientSecret": CLIENT_SECRET,
        "script": data["code"],
        "language": data["language"],
        "versionIndex": data["versionIndex"]
    }

    response = requests.post(
        "https://api.jdoodle.com/v1/execute", json=execution_data)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code,
                            detail="Failed to execute code")

    return response.json()
