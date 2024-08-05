import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app
from pymongo import MongoClient
mongo_client = MongoClient(os.getenv('MONGO_CONNECTION_URI'))  # Adjust connection details
db = mongo_client.get_database('seek-next')   # Adjust database name
client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World from Seek Next!"}

def setup_module():
    # Setup initial data
    db['code_info'].insert_many([
        {
            "problem_id": "wxyz",
            "total_test_cases": "1",
            "test_cases": [
                {
                    "input": "hello",
                    "expected_output": "hello"
                }
            ]
        }
    ])

def teardown_module():
    # Cleanup test data
    db['code_info'].delete_many({"problem_id": {"$in": ["wxyz"]}})
    db['user_code'].delete_many({"user_id": {"$in": ["wxyz"]}})

def test_compute_code_python():
    '''
        Test compute code functionality for Python language.
    '''
    response = client.post(
        "/compute",
        json={
            "problem_id": "wxyz",
            "user_id": "1",
            "language": "python",
            "code": """import sys
class Solution:
    def print_statement(s):
        print(s)

def main():
    # Read input from stdin
    input_data = sys.stdin.read().strip()
    Solution.print_statement(input_data)

if __name__ == "__main__":
    main()
"""
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Passed 1 out of 1 test cases"
    assert len(data["result"]) == 1
    assert data["result"][0]["error"] == "Test case passed"
    assert data["result"][0]["input_data"] == "hello"
    assert data["result"][0]["expected_output"] == "hello"
    assert data["result"][0]["your_output"] == "hello\n"

def test_compute_code_java():
    '''
        Test compute code functionality for Java language.
    '''
    response = client.post(
        "/compute",
        json={
            "problem_id": "wxyz",
            "user_id": "1",
            "language": "java",
            "code": """import java.util.Scanner;

public class solution {
    public static void main(String[] args) {
        // Create a Scanner object to read input from stdin
        Scanner scanner = new Scanner(System.in);

        // Read all input from stdin
        StringBuilder inputBuilder = new StringBuilder();
        while (scanner.hasNextLine()) {
            inputBuilder.append(scanner.nextLine());
            if (scanner.hasNextLine()) {
                inputBuilder.append("\\n");
            }
        }
        String inputData = inputBuilder.toString().trim();

        // Print the input
        System.out.print(inputData);

        // Close the scanner
        scanner.close();
    }
}
"""
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Passed 1 out of 1 test cases"
    assert len(data["result"]) == 1
    assert data["result"][0]["error"] == "Test case passed"
    assert data["result"][0]["input_data"] == "hello"
    assert data["result"][0]["expected_output"] == "hello"
    assert data["result"][0]["your_output"] == "hello"

def test_compute_code_invalid_python_code():
    '''
        Test compute code functionality with invalid Python code.
    '''
    response = client.post(
        "/compute",
        json={
            "problem_id": "wxyz",
            "user_id": "1",
            "language": "python",
            "code": """import sys
class Solution:
    def print_statement(s):
        print(s)

def main():
    # Read input from stdin
    input_data = sys.stdin.read().strip()
    Solution.print_statement(input_data

if __name__ == "__main__":
    main()
"""
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Passed 0 out of 1 test cases"
    assert len(data["result"]) == 1
    assert "SyntaxError" in data["result"][0]["error"]  # Expecting a syntax error
    assert data["result"][0]["input_data"] == "hello"
    assert data["result"][0]["expected_output"] == "hello"
    assert data["result"][0]["your_output"] == ""

def test_compute_code_invalid_java_code():
    '''
        Test compute code functionality with invalid Java code.
    '''
    response = client.post(
        "/compute",
        json={
            "problem_id": "1",
            "user_id": "1",
            "language": "java",
            "code": """import java.util.Scanner;

public class solution {
    public static void main(String[] args) {
        // Create a Scanner object to read input from stdin
        Scanner scanner = new Scanner(System.in);

        // Read all input from stdin
        StringBuilder inputBuilder = new StringBuilder();
        while (scanner.hasNextLine()) {
            inputBuilder.append(scanner.nextLine());
            if (scanner.hasNextLine()) {
                inputBuilder.append("\\n");
            }
        }
        String inputData = inputBuilder.toString().trim();

        // Print the input
        System.out.print(inputData)

        // Close the scanner
        scanner.close();
    }
}
"""
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Passed 0 out of 1 test cases"
    assert len(data["result"]) == 1
    assert "exit status 1" in data["result"][0]["error"]  # Expecting a compilation error
    assert data["result"][0]["input_data"] == "hello"
    assert data["result"][0]["expected_output"] == "hello"
    assert data["result"][0]["your_output"] == ""

def test_compute_code_no_problem_info():
    '''
        Test compute code functionality when problem information does not exist.
    '''
    response = client.post(
        "/compute",
        json={
            "problem_id": "pro",  # Problem ID that does not exist
            "user_id": "1",
            "language": "python",
            "code": """import sys
class Solution:
    def print_statement(s):
        print(s)

def main():
    # Read input from stdin
    input_data = sys.stdin.read().strip()
    Solution.print_statement(input_data)

if __name__ == "__main__":
    main()
"""
        }
    )
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Problem not found"

def test_compute_code_empty_problem_id():
    '''
        Test compute code functionality with an empty problem_id.
    '''
    response = client.post(
        "/compute",
        json={
            "problem_id": "",  # Empty problem ID
            "user_id": "1",
            "language": "python",
            "code": """import sys
class Solution:
    def print_statement(s):
        print(s)

def main():
    # Read input from stdin
    input_data = sys.stdin.read().strip()
    Solution.print_statement(input_data)

if __name__ == "__main__":
    main()
"""
        }
    )
    assert response.status_code == 404  # Unprocessable Entity due to validation error


# def test_compute_code_python():
#     """
#     Test the main endpoint of the API.

#     This test checks if the root endpoint returns a 200 status code
#     and the correct JSON response.
#     """
#     response = client.post(
#         "/compute",
#         json={
#             "code": (
#                 "import sys\n"
#                 "class Solution:\n"
#                 "    def print_statement(s):\n"
#                 "        print(\"s\",s)\n"
#                 "def main():\n"
#                 "    # Read input from stdin\n"
#                 "    input_data = sys.stdin.read().strip()\n"
#                 "    Solution.print_statement(input_data)\n"
#                 "if __name__ == \"__main__\":     main()"
#             ),
#             "user_id": "1",
#             "language": "python",
#             "problem_id": "1"
#         }
#     )
#     assert response.status_code == 200
#     data = response.json()
#     assert "message" in data
#     assert "result" in data
#     assert data["message"] == "Passed 0 out of 2 test cases"
#     assert len(data["result"]) == 2
#     assert data["result"][0]["error"] == "Test case failed"
#     assert data["result"][0]["input_data"] == "hello"
#     assert data["result"][0]["expected_output"] == "hello"
#     assert data["result"][0]["your_output"] == "s hello\n"
#     assert data["result"][1]["error"] == "Test case failed"
#     assert data["result"][1]["input_data"] == "world"
#     assert data["result"][1]["expected_output"] == "world"
#     assert data["result"][1]["your_output"] == "s world\n"

# def test_compute_code_java():
#     response = client.post(
#         "/compute",
#         json={
#             "code": (
#                 "import java.util.Scanner;\n\n"
#                 "public class solution {\n"
#                 "    public static void main(String[] args) {\n"
#                 "        // Create a Scanner object to read input from stdin\n"
#                 "        Scanner scanner = new Scanner(System.in);\n"
#                 "        \n"
#                 "        // Read all input from stdin\n"
#                 "        StringBuilder inputBuilder = new StringBuilder();\n"
#                 "        while (scanner.hasNextLine()) {\n"
#                 "            inputBuilder.append(scanner.nextLine());\n"
#                 "            if (scanner.hasNextLine()) {\n"
#                 "                inputBuilder.append(\"\\n\");\n"
#                 "            }\n"
#                 "        }\n"
#                 "        String inputData = inputBuilder.toString().trim();\n"
#                 "        \n"
#                 "        // Print the input\n"
#                 "        // Print an additional statement\n"
#                 "        // Use the input in another statement\n"
#                 "// Close the scanner\n"
#                 "        scanner.close();\n"
#                 "        System.out.print(inputData);\n"
#                 "    }\n"
#                 "}"
#             ),
#             "user_id": "1",
#             "language": "java",
#             "problem_id": "1"
#         }
#     )
#     assert response.status_code == 200
#     data = response.json()
#     assert "message" in data
#     assert "result" in data
#     assert data["message"] == "Passed 2 out of 2 test cases"
#     assert len(data["result"]) == 2
#     assert data["result"][0]["error"] == "Test case passed"
#     assert data["result"][0]["input_data"] == "hello"
#     assert data["result"][0]["expected_output"] == "hello"
#     assert data["result"][0]["your_output"] == "hello"
#     assert data["result"][1]["error"] == "Test case passed"
#     assert data["result"][1]["input_data"] == "world"
#     assert data["result"][1]["expected_output"] == "world"
#     assert data["result"][1]["your_output"] == "world"


def test_add_code_info():
    '''
        Tests various scenarios for the /add-code-info endpoint.
    '''
    test_id = "test_unique_id"  # Unique identifier for test data

    # Test case 1: Add new code info
    response = client.post(
        "/add-code-info",
        json={
            "problem_id": f"1001_{test_id}",  # Include test_id in problem_id
            "total_test_cases": "1",
            "test_cases": [
                {
                    "input": "hello",
                    "expected_output": "hello"
                }
            ]
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Code information added successfully"

    # Test case 2: Update existing code info
    response = client.post(
        "/add-code-info",
        json={
            "problem_id": f"1001_{test_id}",  # Same problem_id as before
            "total_test_cases": "2",  # Updated value
            "test_cases": [
                {
                    "input": "hello",
                    "expected_output": "hello"
                },
                {
                    "input": "world",
                    "expected_output": "world"
                }
            ]
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Code information updated successfully"

    # Test case 3: Invalid data (missing required fields)
    response = client.post(
        "/add-code-info",
        json={
            "problem_id": f"1002_{test_id}",  # Unique problem_id
            # Missing "total_test_cases" and "test_cases"
        }
    )
    assert response.status_code == 422  # Unprocessable Entity due to validation error

    # Test case 4: Invalid data (incorrect type for total_test_cases)
    response = client.post(
        "/add-code-info",
        json={
            "problem_id": f"1003_{test_id}",  # Unique problem_id
            "total_test_cases": 1,  # Should be a string based on your model
            "test_cases": [
                {
                    "input": "test",
                    "expected_output": "test"
                }
            ]
        }
    )
    assert response.status_code == 422  # Unprocessable Entity due to validation error

    # Test case 5: Edge case with empty test_cases
    response = client.post(
        "/add-code-info",
        json={
            "problem_id": f"1004_{test_id}",  # Unique problem_id
            "total_test_cases": "0",
            "test_cases": []  # Empty list
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Code information added successfully"

    # Cleanup: Delete test documents
    db['code_info'].delete_many({"problem_id": {"$regex": test_id}})

# Test for delete_code_info endpoint
def test_delete_code_info():
    '''
        Tests various scenarios for the /delete-code-info endpoint.
    '''

    # Test case 1: Successfully delete existing code info
    # First, ensure there's a document to delete
    client.post(
        "/add-code-info",
        json={
            "problem_id": "test_delete",
            "total_test_cases": "1",
            "test_cases": [
                {
                    "input": "test",
                    "expected_output": "test"
                }
            ]
        }
    )

    # Now, delete it
    response = client.delete("/delete-code-info?problem_id=test_delete")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Code information deleted successfully"

    # Test case 2: Attempt to delete a non-existent code info
    response = client.delete("/delete-code-info?problem_id=xxx")
    assert response.status_code == 404  # Not Found
    data = response.json()
    assert data["detail"] == "Code information not found"

    # Test case 3: Invalid `problem_id` format (assuming `problem_id` should be a string)
    # You might have validation rules, so adjust as necessary
    response = client.delete("/delete-code-info?problem_id=")  # Empty string
    assert response.status_code == 422  # Unprocessable Entity if validation fails

    # Test case 4: Invalid request (missing `problem_id` parameter)
    response = client.delete("/delete-code-info")  # No query parameter
    assert response.status_code == 422  # Unprocessable Entity if validation fails


if __name__ == "__main__":
    pytest.main()