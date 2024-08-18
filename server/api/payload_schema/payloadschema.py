from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


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
    total_test_cases: str
    test_cases: List[TestCase]

    class Config:
        json_schema_extra = {
            "example": {
                "problem_id": 1,
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


class CourseOverview(BaseModel):
    course_description: str
    assignment_marks: dict
    exam_marks: dict


class ModuleDetails(BaseModel):
    id: int
    title: str
    description: str
    total_lectures: int
    total_assignments: int


class CourseDetails(BaseModel):
    title: str
    description: str
    total_modules: int
    price: float


class EnrollmentResponse(BaseModel):
    message: str


class CourseEnrolled(BaseModel):
    id: int
    title: str


class StudentEnrolled(BaseModel):
    id: int
    username: str


class StudentCourseOverviewRequest(BaseModel):
    course_id: int
    student_id: int


class StudentModuleDetailsRequest(BaseModel):
    course_id: int
    module_id: int


class CreateAssignmentRequest(BaseModel):
    module_id: int
    title: str
    description: str
    type: str
    due_date: datetime


class CourseBase(BaseModel):
    title: str
    description: str
    total_modules: int
    price: float


class CourseCreate(CourseBase):
    pass


class CourseUpdate(CourseBase):
    id: int


class CourseResponse(CourseBase):
    id: int

    class Config:
        from_attributes = True


class AssignmentSubmission(BaseModel):
    student_id: int
    answers: dict
    assignment_answer:str
