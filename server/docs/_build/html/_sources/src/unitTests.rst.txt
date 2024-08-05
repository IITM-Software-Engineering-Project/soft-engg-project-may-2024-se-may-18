Unit Test Documentation
=======================

This document provides details about the unit tests for the API endpoints. Each test case includes information about the API being tested, the inputs, expected output, actual output, and the result.

Test Cases
----------

1. **Test Case: `test_read_main`**

   - **API being tested:** `/`
   - **Inputs:** None
   - **Expected Output:**

     .. code-block:: python

       {
         "message": "Hello World from Seek Next!"
       }

   - **Actual Output:**

     .. code-block:: python

       {
         "message": "Hello World from Seek Next!"
       }

   - **Result:** Success

2. **Test Case: `test_compute_code_python`**

   - **API being tested:** `/compute`
   - **Inputs:**

     .. code-block:: python

       {
         "code": "import sys\nclass Solution:\n    def print_statement(s):\n        print(\"s\",s)\n...\n",
         "user_id": "1",
         "language": "python",
         "problem_id": "1"
       }

   - **Expected Output:**

     .. code-block:: python

       {
         "message": "Passed 0 out of 2 test cases",
         "result": [
           {"error": "Test case failed", "input_data": "hello", "expected_output": "hello", "your_output": "s hello\n"},
           {"error": "Test case failed", "input_data": "world", "expected_output": "world", "your_output": "s world\n"}
         ]
       }

   - **Actual Output:**

     .. code-block:: python

       {
         "message": "Passed 0 out of 2 test cases",
         "result": [
           {"error": "Test case failed", "input_data": "hello", "expected_output": "hello", "your_output": "s hello\n"},
           {"error": "Test case failed", "input_data": "world", "expected_output": "world", "your_output": "s world\n"}
         ]
       }

   - **Result:** Success

3. **Test Case: `test_compute_code_java`**

   - **API being tested:** `/compute`
   - **Inputs:**

     .. code-block:: python

       {
         "code": "import java.util.Scanner;\npublic class solution {\n    public static void main(String[] args) {\n...\n",
         "user_id": "1",
         "language": "java",
         "problem_id": "1"
       }

   - **Expected Output:**

     .. code-block:: python

       {
         "message": "Passed 2 out of 2 test cases",
         "result": [
           {"error": "Test case passed", "input_data": "hello", "expected_output": "hello", "your_output": "hello"},
           {"error": "Test case passed", "input_data": "world", "expected_output": "world", "your_output": "world"}
         ]
       }

   - **Actual Output:**

     .. code-block:: python

       {
         "message": "Passed 2 out of 2 test cases",
         "result": [
           {"error": "Test case passed", "input_data": "hello", "expected_output": "hello", "your_output": "hello"},
           {"error": "Test case passed", "input_data": "world", "expected_output": "world", "your_output": "world"}
         ]
       }

   - **Result:** Success

4. **Test Case: `test_add_code_info`**

   - **API being tested:** `/add-code-info`
   - **Inputs:**

     .. code-block:: python

       {
         "problem_id": "problem123",
         "user_id": "user123",
         "total_test_cases": 3,
         "test_cases": [
           {"input": "input1", "output": "output1"},
           {"input": "input2", "output": "output2"},
           {"input": "input3", "output": "output3"}
         ]
       }

   - **Expected Output:**

     .. code-block:: python

       {
         "message": "Code info added successfully"
       }

   - **Actual Output:**

     .. code-block:: python

       {
         "message": "Code info added successfully"
       }

   - **Result:** Success

5. **Test Case: `test_delete_code_info`**

   - **API being tested:** `/delete-code-info`
   - **Inputs:**

     .. code-block:: python

       {
         "problem_id": "problem123"
       }

   - **Expected Output:**

     .. code-block:: python

       {
         "message": "Code info deleted successfully"
       }

   - **Actual Output:**

     .. code-block:: python

       {
         "message": "Code info deleted successfully"
       }

   - **Result:** Success
