from database.no_sql import get_user_code_collection, get_code_info_collection
from datetime import datetime
from fastapi import APIRouter, HTTPException
from fastapi.requests import Request
import tempfile
import os
import subprocess
from api.payload_schema.payloadschema import ComputeCodeRequest, CodeInfo, DeleteCodeInfoRequest

code_router = APIRouter()


@code_router.post("/compute",
                  description="Compute test cases for submitted code using subprocesses",
                  response_description="Message indicating test case results",
                  tags=["Coding Assignment"],
                  )
async def compute_code(request: ComputeCodeRequest):
    data = request.model_dump()
    code = data["code"]
    user_id = data["user_id"]
    language = data["language"]
    problem_id = data["problem_id"]
    time = datetime.now()
    user_code_collection = get_user_code_collection()
    code_info_collection = get_code_info_collection()
    error_list = []
    # Fetch problem information
    problem_info = code_info_collection.find_one({"problem_id": problem_id})
    if not problem_info:
        raise HTTPException(status_code=404, detail="Problem not found")

    total_test_cases = int(problem_info["total_test_cases"])
    test_cases = problem_info["test_cases"]

    test_cases_passed = 0

    # Create a temporary directory to store the user's code
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a 'code' subdirectory
        code_dir = os.path.join(temp_dir, 'code')
        os.makedirs(code_dir)

        # Write user code to a file in the 'code' subdirectory
        code_file_name = f"solution.{get_file_extension(language)}"
        code_file_path = os.path.join(code_dir, code_file_name)
        with open(code_file_path, 'w') as code_file:
            code_file.write(code)

        for i, test_case in enumerate(test_cases):
            input_data = test_case["input"]
            expected_output = test_case["output"]

            # Run the code using subprocess
            try:
                output = ""
                output = run_code_with_subprocess(
                    language, code_dir, code_file_name, input_data)

                # Compare output with expected output
                if output.strip() == expected_output.strip():
                    test_cases_passed += 1
                    error_list.append({
                        "error": "Test case passed",
                        "input_data": input_data,
                        "expected_output": expected_output,
                        "your_output": output
                    })
                else:
                    print(f'''Test case {i} failed. Expected: {
                          expected_output}, Got: {output}''')
                    error_list.append({
                        "error": "Test case failed",
                        "input_data": input_data,
                        "expected_output": expected_output,
                        "your_output": output
                    })
            except Exception as e:
                # Log the error and continue with the next test case
                error_list.append({
                    "error": str(e),
                    "input_data": input_data,
                    "expected_output": expected_output,
                    "your_output": output
                })
                print(f"Error running test case {i}: {str(e)}")
    filter_query = {
        "problem_id": problem_id,
        "user_id": user_id
    }
    update_operation = {
        "$set": {
            "code": code,
            "language": language,
            "test_cases_passed": test_cases_passed,
            "total_test_cases": total_test_cases,
            "submitted_at": time,
            "result": error_list
        }
    }
    res =  user_code_collection.update_one(
        filter_query,
        update_operation,
        upsert=True
    )

    return {
        "message": f"Passed {test_cases_passed} out of {total_test_cases} test cases",
        "result": error_list
    }


def get_file_extension(language):
    extensions = {
        "python": "py",
        "java": "java",
        "javascript": "js",
        # Add more languages as needed
    }
    return extensions.get(language, "txt")


def run_code_with_subprocess(language, code_dir, code_file_name, input_data):
    if language == "python":
        command = ["python3", os.path.join(code_dir, code_file_name)]
    elif language == "java":
        class_name = code_file_name.split('.')[0]
        compile_command = ["javac", os.path.join(code_dir, code_file_name)]
        subprocess.run(compile_command, cwd=code_dir, check=True)
        command = ["java", "-cp", code_dir, class_name]
    elif language == "javascript":
        command = ["node", os.path.join(code_dir, code_file_name)]
    else:
        raise ValueError(f"Unsupported language: {language}")
    try:
        process = subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=code_dir
        )
        stdout, stderr = process.communicate(
            input=input_data, timeout=5)  # 5 second timeout

        if process.returncode != 0:
            raise RuntimeError(f"Code execution failed: {stderr}")

        return stdout
    except subprocess.TimeoutExpired:
        process.kill()
        raise RuntimeError("Code execution timed out")


@code_router.post("/add-code-info",
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


@code_router.delete("/delete-code-info",
                    description="Delete code information from the database",
                    response_description="Code information deleted successfully",
                    tags=["Coding Assignment","Instructor"])
async def delete_code_info(problem_id: str):
    # data = request.model_dump()  # Convert Pydantic model to dictionary

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
