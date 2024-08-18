from fastapi import APIRouter, HTTPException, Request, Query
from database.no_sql import get_user_code_collection, get_code_info_collection
from pydantic import BaseModel
from api.payload_schema.payloadschema import CodeInfo
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
    # print(data)
    
    # Retrieve the CodeInfo document for the given problem_id
    code_info_collection = get_code_info_collection()
    code_info = code_info_collection.find_one({"problem_id": data["problem_id"]})
    
    if not code_info:
        raise HTTPException(status_code=404, detail="Problem not found")
    
    test_results = []
    
    for test_case in code_info['test_cases']:
        execution_data = {
            "clientId": CLIENT_ID,
            "clientSecret": CLIENT_SECRET,
            "script": data["code"],
            "language": data["language"],
            "versionIndex": data.get("versionIndex", "0"),  # Default version index if not provided
            "stdin": test_case["input"]
        }

        response = requests.post("https://api.jdoodle.com/v1/execute", json=execution_data)

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to execute code")

        actual_output = response.json().get("output", "").strip()
        expected_output = test_case["expected_output"].strip()

        test_results.append({
            "input": test_case["input"],
            "expected_output": expected_output,
            "actual_output": actual_output,
            "passed": actual_output == expected_output
        })
    
    return {"results": test_results}


@code_runner_router.post("/add-code-info",
                  description="Add or update code information in the database",
                  response_description="Code information added or updated successfully",
                  tags=["Coding Assignment", "Instructor"])
async def add_code_info(request: CodeInfo):
    data = request.model_dump()  # Convert Pydantic model to dictionary

    code_info_collection = get_code_info_collection()

    # Define the filter to find the document by problem_id
    filter_query = {
        "problem_id": data["problem_id"]
    }
    # Define the update operation
    update_operation = {
        "$set": {
            "total_test_cases": data["total_test_cases"],
            "test_cases": data["test_cases"]
        }
    }

    # Perform the update with upsert
    result = code_info_collection.update_one(
        filter_query,
        update_operation,
        upsert=True
    )

    if result.matched_count > 0:
        return {
            "message": "Code information updated successfully"
        }
    else:
        return {
            "message": "Code information added successfully"
        }


@code_runner_router.delete("/delete-code-info",
                    description="Delete code information from the database",
                    response_description="Code information deleted successfully",
                    tags=["Coding Assignment","Instructor"])
async def delete_code_info(problem_id: str = Query(..., min_length=1, description="The ID of the problem to delete")):
    # data = request.model_dump()  # Convert Pydantic model to dictionary
    if not problem_id.strip():
        raise HTTPException(
            status_code=422,
            detail="Problem ID must not be empty"
        )

    code_info_collection = get_code_info_collection()

    # Define the filter to find the document by problem_id
    filter_query = {
        "problem_id": problem_id
    }

    # Perform the deletion
    result = code_info_collection.delete_one(filter_query)

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404, detail="Code information not found")

    return {
        "message": "Code information deleted successfully"
    }

