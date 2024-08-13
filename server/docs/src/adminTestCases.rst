Extended Course API Test Cases
===============================

This document provides details about the additional unit tests for the course-related API endpoints. Each test case includes information about the API being tested, the inputs, expected output, actual output, and the result.

**Test Cases for `/courses/create`**
--------------------------------------

**Test Case: `test_create_course`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   - **API being tested:** `/courses/create`
   - **Inputs:**

     .. code-block:: json

       {
         "title": "New Test Course 1",
         "description": "A new test course description",
         "total_modules": 10,
         "price": 100.0
       }

   - **Expected Output:**
     - Ensure the response contains the details of the newly created course.

   - **Actual Output:**

     .. code-block:: json

       {
         "title": "New Test Course 1",
         "description": "A new test course description",
         "total_modules": 10,
         "price": 100.0
       }

   - **Result:** Success

**Test Case: `test_create_course_missing_fields`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   - **API being tested:** `/courses/create`
   - **Inputs:**

     .. code-block:: json

       {
         "title": "Incomplete Course",
         "description": "Missing total_modules and price"
       }

   - **Expected Output:**

     .. code-block:: json

       {
         "detail": "Unprocessable Entity (Validation error)"
       }

   - **Actual Output:**

     .. code-block:: json

       {
         "detail": "Unprocessable Entity (Validation error)"
       }

   - **Result:** Success

**Test Case: `test_create_course_invalid_data_type`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   - **API being tested:** `/courses/create`
   - **Inputs:**

     .. code-block:: json

       {
         "title": "Invalid Course",
         "description": "Invalid data types",
         "total_modules": "ten",
         "price": "hundred"
       }

   - **Expected Output:**

     .. code-block:: json

       {
         "detail": "Unprocessable Entity (Validation error)"
       }

   - **Actual Output:**

     .. code-block:: json

       {
         "detail": "Unprocessable Entity (Validation error)"
       }

   - **Result:** Success

**Test Cases for `/courses/update`**
--------------------------------------

**Test Case: `test_update_course`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   - **API being tested:** `/courses/update`
   - **Inputs:**

     .. code-block:: json

       {
         "id": 1,
         "title": "Updated Test Course",
         "description": "An updated test course description"
       }

   - **Expected Output:**
     - Ensure the response contains the updated details of the course.

   - **Actual Output:**

     .. code-block:: json

       {
         "id": 1,
         "title": "Updated Test Course",
         "description": "An updated test course description"
       }

   - **Result:** Success

**Test Case: `test_update_non_existent_course`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   - **API being tested:** `/courses/update`
   - **Inputs:**

     .. code-block:: json

       {
         "id": 9999,
         "title": "Non-existent Course",
         "description": "Should not be updated"
       }

   - **Expected Output:**

     .. code-block:: json

       {
         "detail": "Course not found"
       }

   - **Actual Output:**

     .. code-block:: json

       {
         "detail": "Course not found"
       }

   - **Result:** Success

**Test Case: `test_update_course_invalid_id`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   - **API being tested:** `/courses/update`
   - **Inputs:**

     .. code-block:: json

       {
         "id": 2000,
         "title": "Invalid ID Course",
         "description": "Should fail due to invalid ID"
       }

   - **Expected Output:**

     .. code-block:: json

       {
         "detail": "Course not found"
       }

   - **Actual Output:**

     .. code-block:: json

       {
         "detail": "Course not found"
       }

   - **Result:** Success

**Test Cases for `/courses/delete`**
--------------------------------------

**Test Case: `test_delete_course`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   - **API being tested:** `/courses/delete`
   - **Inputs:**

     .. code-block:: json

       {
         "id": 1
       }

   - **Expected Output:**

     .. code-block:: json

       {
         "message": "Course deleted successfully"
       }

   - **Actual Output:**

     .. code-block:: json

       {
         "message": "Course deleted successfully"
       }

   - **Result:** Success

**Test Case: `test_delete_non_existent_course`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   - **API being tested:** `/courses/delete`
   - **Inputs:**

     .. code-block:: json

       {
         "id": 9999
       }

   - **Expected Output:**

     .. code-block:: json

       {
         "detail": "Course not found"
       }

   - **Actual Output:**

     .. code-block:: json

       {
         "detail": "Course not found"
       }

   - **Result:** Success

**Test Cases for `/courses/get`**
--------------------------------------

**Test Case: `test_get_course`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   - **API being tested:** `/courses/get`
   - **Inputs:**

     .. code-block:: json

       {
         "id": 1
       }

   - **Expected Output:**
     - Ensure the response contains the details of the course with the given ID.

   - **Actual Output:**

     .. code-block:: json

       {
         "id": 1,
         "title": "Test Course",
         "description": "A test course description"
       }

   - **Result:** Success

**Test Case: `test_get_course_invalid_id`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   - **API being tested:** `/courses/get`
   - **Inputs:**

     .. code-block:: json

       {
         "id": "invalid_id"
       }

   - **Expected Output:**

     .. code-block:: json

       {
         "detail": "Unprocessable Entity (Validation error)"
       }

   - **Actual Output:**

     .. code-block:: json

       {
         "detail": "Unprocessable Entity (Validation error)"
       }

   - **Result:** Success

**Test Cases for `/courses/list`**
--------------------------------------

**Test Case: `test_get_all_courses`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   - **API being tested:** `/courses/list`
   - **Inputs:**

     .. code-block:: json

       {}

   - **Expected Output:**
     - Ensure the response contains a list of all courses.

   - **Actual Output:**

     .. code-block:: json

       [
         {
           "id": 1,
           "title": "New Test Course 1",
           "description": "A new test course description",
           "total_modules": 10,
           "price": 100.0
         }
       ]

   - **Result:** Success

**Test Case: `test_get_all_courses_pagination`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   - **API being tested:** `/courses/list`
   - **Inputs:**

     .. code-block:: json

       {
         "limit": 5,
         "skip": 5
       }

   - **Expected Output:**
     - Ensure the response contains a paginated list of courses.

   - **Actual Output:**

     .. code-block:: json

       [
         {
           "id": 9,
           "title": "Course 9",
           "description": "Course description",
           "total_modules": 10,
           "price": 100.0
         }
       ]

   - **Result:** Success

**Test Case: `test_get_all_courses_no_data`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   - **API being tested:** `/courses/list`
   - **Inputs:**

     .. code-block:: json

       {}

   - **Expected Output:**

     .. code-block:: json

       {
         "courses": []
       }

   - **Actual Output:**

     .. code-block:: json

       {
         "courses": []
       }

   - **Result:** Success
