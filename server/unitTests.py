import pytest
from fastapi.testclient import TestClient

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
    response = client.post(
        "/add-code-info",
        json={
            "problem_id": "problem123",
            "user_id": "user123",
            "total_test_cases": 3,
            "test_cases": [
                {"input": "input1", "output": "output1"},
                {"input": "input2", "output": "output2"},
                {"input": "input3", "output": "output3"}
            ]
        }
    )
    assert response.status_code == 200
    assert "message" in response.json()

# Test for delete_code_info endpoint
def test_delete_code_info():
    # First, add code info to ensure there's something to delete
    client.post(
        "/add-code-info",
        json={
            "problem_id": "problem123",
            "user_id": "user123",
            "total_test_cases": 3,
            "test_cases": [
                {"input": "input1", "output": "output1"},
                {"input": "input2", "output": "output2"},
                {"input": "input3", "output": "output3"}
            ]
        }
    )

    # Now delete the code info
    response = client.delete(
        "/delete-code-info",
        params={"problem_id": "problem123"}
    )
    assert response.status_code == 200
    assert "message" in response.json()

    # Verify that the code info was actually deleted
    response = client.post(
        "/compute",
        json={
            "code": "print('Hello, World!')",
            "user_id": "user123",
            "language": "python",
            "problem_id": "problem123"
        }
    )
    assert response.status_code == 404
    assert response.json().get("detail") == "Problem not found"


if __name__ == "__main__":
    pytest.main()