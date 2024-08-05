import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World from Seek Next!"}


def test_compute_code_python():
    """
    Test the main endpoint of the API.

    This test checks if the root endpoint returns a 200 status code
    and the correct JSON response.
    """
    response = client.post(
        "/compute",
        json={
            "code": (
                "import sys\n"
                "class Solution:\n"
                "    def print_statement(s):\n"
                "        print(\"s\",s)\n"
                "def main():\n"
                "    # Read input from stdin\n"
                "    input_data = sys.stdin.read().strip()\n"
                "    Solution.print_statement(input_data)\n"
                "if __name__ == \"__main__\":     main()"
            ),
            "user_id": "1",
            "language": "python",
            "problem_id": "1"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "result" in data
    assert data["message"] == "Passed 0 out of 2 test cases"
    assert len(data["result"]) == 2
    assert data["result"][0]["error"] == "Test case failed"
    assert data["result"][0]["input_data"] == "hello"
    assert data["result"][0]["expected_output"] == "hello"
    assert data["result"][0]["your_output"] == "s hello\n"
    assert data["result"][1]["error"] == "Test case failed"
    assert data["result"][1]["input_data"] == "world"
    assert data["result"][1]["expected_output"] == "world"
    assert data["result"][1]["your_output"] == "s world\n"

def test_compute_code_java():
    response = client.post(
        "/compute",
        json={
            "code": (
                "import java.util.Scanner;\n\n"
                "public class solution {\n"
                "    public static void main(String[] args) {\n"
                "        // Create a Scanner object to read input from stdin\n"
                "        Scanner scanner = new Scanner(System.in);\n"
                "        \n"
                "        // Read all input from stdin\n"
                "        StringBuilder inputBuilder = new StringBuilder();\n"
                "        while (scanner.hasNextLine()) {\n"
                "            inputBuilder.append(scanner.nextLine());\n"
                "            if (scanner.hasNextLine()) {\n"
                "                inputBuilder.append(\"\\n\");\n"
                "            }\n"
                "        }\n"
                "        String inputData = inputBuilder.toString().trim();\n"
                "        \n"
                "        // Print the input\n"
                "        // Print an additional statement\n"
                "        // Use the input in another statement\n"
                "// Close the scanner\n"
                "        scanner.close();\n"
                "        System.out.print(inputData);\n"
                "    }\n"
                "}"
            ),
            "user_id": "1",
            "language": "java",
            "problem_id": "1"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "result" in data
    assert data["message"] == "Passed 2 out of 2 test cases"
    assert len(data["result"]) == 2
    assert data["result"][0]["error"] == "Test case passed"
    assert data["result"][0]["input_data"] == "hello"
    assert data["result"][0]["expected_output"] == "hello"
    assert data["result"][0]["your_output"] == "hello"
    assert data["result"][1]["error"] == "Test case passed"
    assert data["result"][1]["input_data"] == "world"
    assert data["result"][1]["expected_output"] == "world"
    assert data["result"][1]["your_output"] == "world"

def test_add_code_info():
    '''
        Adds information of a code to the database if the problem id does not exist else updates the information.
        The output is of string format as it is required for the students to print the final output of the problem.
    '''

    # Test case 1: Add new code info
    response = client.post(
        "/add-code-info",
        json={
            "problem_id": "2",
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
            "problem_id": "2",  # Same problem_id as before
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
            "problem_id": "3",
            # Missing "total_test_cases" and "test_cases"
        }
    )
    assert response.status_code == 422  # Unprocessable Entity due to validation error

    # Test case 4: Invalid data (incorrect type for total_test_cases)
    response = client.post(
        "/add-code-info",
        json={
            "problem_id": "4",
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
            "problem_id": "5",
            "total_test_cases": "0",
            "test_cases": []  # Empty list
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Code information added successfully"

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
            "problem_id": "6",
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
    response = client.delete("/delete-code-info?problem_id=6")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Code information deleted successfully"

    # Test case 2: Attempt to delete a non-existent code info
    response = client.delete("/delete-code-info?problem_id=7")
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