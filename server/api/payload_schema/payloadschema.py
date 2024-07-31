from pydantic import BaseModel
from typing import List


class ComputeCodeRequest(BaseModel):
    code: str
    user_id: str
    language: str
    problem_id: str

    class Config:
        json_schema_extra = {
            "example": {
                "code": "import sys\nclass Solution:\n    def print_statement(s):\n        print(s)\ndef main():\n    # Read input from stdin\n    input_data = sys.stdin.read().strip()\n    Solution.print_statement(input_data)\nif __name__ == \"__main__\":     main() ",
                "user_id": "1",
                "language": "python",
                "problem_id": "1"
            }
        }


class TestCase(BaseModel):
    input: str
    expected_output: str

    class Config:
        json_schema_extra = {
            "example": {
                "input": "1",
                "expected_output": "1"
            }
        }


class CodeInfo(BaseModel):
    problem_id: str
    user_id: str
    total_test_cases: str
    test_cases: List[TestCase]

    class Config:
        json_schema_extra = {
            "example": {
                "problem_id": 1,
                "user_id": 1,
                "total_test_cases": 1,
                "test_cases": [
                    {
                        "input": "1",
                        "expected_output": "1"
                    }
                ]
            }
        }


class DeleteCodeInfoRequest(BaseModel):
    problem_id: str
