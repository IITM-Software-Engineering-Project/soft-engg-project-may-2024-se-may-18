Code Computation Service Test Cases
====================================

This document provides details about the unit tests for the API endpoints related to code submissions. Each test case includes information about the API being tested, the inputs, expected output, actual output, and the result.


**Test Cases for `/compute`**
-----------------------------------

**Test Case: `test_compute_code_python`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   - **API being tested:** `/compute`
   - **Inputs:**

     .. code-block:: json

       {
         "problem_id": "wxyz",
         "user_id": "1",
         "language": "python",
         "code": "import sys\nclass Solution:\n    def print_statement(s):\n        print(s)\n\ndef main():\n    # Read input from stdin\n    input_data = sys.stdin.read().strip()\n    Solution.print_statement(input_data)\n\nif __name__ == \"__main__\":\n    main()"
       }

   - **Expected Output:**

     .. code-block:: json

       {
         "message": "Passed 1 out of 1 test cases",
         "result": [
           {"error": "Test case passed", "input_data": "hello", "expected_output": "hello", "your_output": "hello\n"}
         ]
       }

   - **Actual Output:**

     .. code-block:: json

       {
         "message": "Passed 1 out of 1 test cases",
         "result": [
           {"error": "Test case passed", "input_data": "hello", "expected_output": "hello", "your_output": "hello\n"}
         ]
       }

   - **Result:** Success


**Test Case: `test_compute_code_java`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   - **API being tested:** `/compute`
   - **Inputs:**

     .. code-block:: json

       {
         "problem_id": "wxyz",
         "user_id": "1",
         "language": "java",
         "code": "import java.util.Scanner;\n\npublic class solution {\n    public static void main(String[] args) {\n        // Create a Scanner object to read input from stdin\n        Scanner scanner = new Scanner(System.in);\n\n        // Read all input from stdin\n        StringBuilder inputBuilder = new StringBuilder();\n        while (scanner.hasNextLine()) {\n            inputBuilder.append(scanner.nextLine());\n            if (scanner.hasNextLine()) {\n                inputBuilder.append(\"\\n\");\n            }\n        }\n        String inputData = inputBuilder.toString().trim();\n\n        // Print the input\n        System.out.print(inputData);\n\n        // Close the scanner\n        scanner.close();\n    }\n}"
       }

   - **Expected Output:**

     .. code-block:: json

       {
         "message": "Passed 1 out of 1 test cases",
         "result": [
           {"error": "Test case passed", "input_data": "hello", "expected_output": "hello", "your_output": "hello"}
         ]
       }

   - **Actual Output:**

     .. code-block:: json

       {
         "message": "Passed 1 out of 1 test cases",
         "result": [
           {"error": "Test case passed", "input_data": "hello", "expected_output": "hello", "your_output": "hello"}
         ]
       }

   - **Result:** Success


**Test Case: `test_compute_code_invalid_python_code`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   - **API being tested:** `/compute`
   - **Inputs:**

     .. code-block:: json

       {
         "problem_id": "wxyz",
         "user_id": "1",
         "language": "python",
         "code": "import sys\nclass Solution:\n    def print_statement(s):\n        print(s)\n\ndef main():\n    # Read input from stdin\n    input_data = sys.stdin.read().strip()\n    Solution.print_statement(input_data\n\nif __name__ == \"__main__\":\n    main()"
       }

   - **Expected Output:**

     .. code-block:: json

       {
         "message": "Passed 0 out of 1 test cases",
         "result": [
           {"error": "SyntaxError", "input_data": "hello", "expected_output": "hello", "your_output": ""}
         ]
       }

   - **Actual Output:**

     .. code-block:: json

       {
         "message": "Passed 0 out of 1 test cases",
         "result": [
           {"error": "SyntaxError", "input_data": "hello", "expected_output": "hello", "your_output": ""}
         ]
       }

   - **Result:** Success


**Test Case: `test_compute_code_invalid_java_code`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   - **API being tested:** `/compute`
   - **Inputs:**

     .. code-block:: json

       {
         "problem_id": "1",
         "user_id": "1",
         "language": "java",
         "code": "import java.util.Scanner;\n\npublic class solution {\n    public static void main(String[] args) {\n        // Create a Scanner object to read input from stdin\n        Scanner scanner = new Scanner(System.in);\n\n        // Read all input from stdin\n        StringBuilder inputBuilder = new StringBuilder();\n        while (scanner.hasNextLine()) {\n            inputBuilder.append(scanner.nextLine());\n            if (scanner.hasNextLine()) {\n                inputBuilder.append(\"\\n\");\n            }\n        }\n        String inputData = inputBuilder.toString().trim();\n\n        // Print the input\n        System.out.print(inputData)\n\n        // Close the scanner\n        scanner.close();\n    }\n}"
       }

   - **Expected Output:**

     .. code-block:: json

       {
         "message": "Passed 0 out of 1 test cases",
         "result": [
           {"error": "Compilation error", "input_data": "hello", "expected_output": "hello", "your_output": ""}
         ]
       }

   - **Actual Output:**

     .. code-block:: json

       {
         "message": "Passed 0 out of 1 test cases",
         "result": [
           {"error": "Compilation error", "input_data": "hello", "expected_output": "hello", "your_output": ""}
         ]
       }

   - **Result:** Success


**Test Case: `test_compute_code_no_problem_info`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   - **API being tested:** `/compute`
   - **Inputs:**

     .. code-block:: json

       {
         "problem_id": "pro",
         "user_id": "1",
         "language": "python",
         "code": "import sys\nclass Solution:\n    def print_statement(s):\n        print(s)\n\ndef main():\n    # Read input from stdin\n    input_data = sys.stdin.read().strip()\n    Solution.print_statement(input_data)\n\nif __name__ == \"__main__\":\n    main()"
       }

   - **Expected Output:**

     .. code-block:: json

       {
         "detail": "Problem not found"
       }

   - **Actual Output:**

     .. code-block:: json

       {
         "detail": "Problem not found"
       }

   - **Result:** Success


**Test Case: `test_compute_code_empty_problem_id`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   - **API being tested:** `/compute`
   - **Inputs:**

     .. code-block:: json

       {
         "problem_id": "",
         "user_id": "1",
         "language": "python",
         "code": "import sys\nclass Solution:\n    def print_statement(s):\n        print(s)\n\ndef main():\n    # Read input from stdin\n    input_data = sys.stdin.read().strip()\n    Solution.print_statement(input_data)\n\nif __name__ == \"__main__\":\n    main()"
       }

   - **Expected Output:**

     .. code-block:: json

       {
         "detail": "Invalid input"
       }

   - **Actual Output:**

     .. code-block:: json

       {
         "detail": "Invalid input"
       }

   - **Result:** Success


**Test Cases for `/add-code-info`**
------------------------------------------

**Test Case: `test_add_code_info`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   - **API being tested:** `/add-code-info`
   - **Inputs:**

     .. code-block:: json

       {
         "problem_id": "1001_test_unique_id",
         "total_test_cases": "1",
         "test_cases": [
           {"input": "hello", "expected_output": "hello"}
         ]
       }

   - **Expected Output:**

     .. code-block:: json

       {
         "message": "Code information added successfully"
       }

   - **Actual Output:**

     .. code-block:: json

       {
         "message": "Code information added successfully"
       }

   - **Result:** Success


**Test Case: `test_add_code_info_missing_problem_id`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   - **API being tested:** `/add-code-info`
   - **Inputs:**

     .. code-block:: json

       {
         "problem_id": "",
         "total_test_cases": "1",
         "test_cases": [
           {"input": "hello", "expected_output": "hello"}
         ]
       }

   - **Expected Output:**

     .. code-block:: json

       {
         "detail": "Problem ID is required"
       }

   - **Actual Output:**

     .. code-block:: json

       {
         "detail": "Problem ID is required"
       }

   - **Result:** Success


**Test Cases for `/delete-code-info`**
--------------------------------------------

**Test Case: `test_delete_code_info`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   - **API being tested:** `/delete-code-info`
   - **Inputs:**

     .. code-block:: json

       {
         "problem_id": "1001_test_unique_id"
       }

   - **Expected Output:**

     .. code-block:: json

       {
         "message": "Code information deleted successfully"
       }

   - **Actual Output:**

     .. code-block:: json

       {
         "message": "Code information deleted successfully"
       }

   - **Result:** Success


**Test Case: `test_delete_code_info_not_found`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   - **API being tested:** `/delete-code-info`
   - **Inputs:**

     .. code-block:: json

       {
         "problem_id": "non_existing_problem_id"
       }

   - **Expected Output:**

     .. code-block:: json

       {
         "detail": "Code information not found"
       }

   - **Actual Output:**

     .. code-block:: json

       {
         "detail": "Code information not found"
       }

   - **Result:** Success

