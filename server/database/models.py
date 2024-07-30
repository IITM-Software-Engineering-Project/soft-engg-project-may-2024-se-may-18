from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, sessionmaker
from database.db_sql import init_db
from pydantic import BaseModel
from typing import List

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    role = Column(String(50), nullable=False)
    last_login = Column(DateTime, nullable=False)
    email = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)



class Content(Base):
    __tablename__ = 'contents'

    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    week_no=Column(Integer, nullable=False)
    link = Column(String(50), nullable=False)

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


engine = None

if not engine:
    engine = init_db()
    Base.metadata.create_all(engine, checkfirst=True)
    session = sessionmaker(bind=engine)
    print("SQL Database connected Successfully.")
