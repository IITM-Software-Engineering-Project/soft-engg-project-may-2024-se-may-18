Student Course Management API Unit Tests
==========================================

This document provides details about the unit tests for the API endpoints related to student course management. Each test case includes information about the API being tested, the inputs, expected output, actual output, and the result.

**Test Cases for `/student/enrolled_course/student-overview`**
-------------------------------------------------------------------

**Test Case: `test_get_student_course_overview_success`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   - **Inputs:**

     .. code-block:: json

       {
         "course_id": "1",
         "student_id": "1"
       }

   - **Expected Output:**

     .. code-block:: json

       {
         "course_description": "Test Description",
         "assignment_marks": {"1": null},
         "exam_marks": {"1": 90.0}
       }

   - **Actual Output:**

     .. code-block:: json

       {
         "course_description": "Test Description",
         "assignment_marks": {"1": null},
         "exam_marks": {"1": 90.0}
       }

   - **Result:** Success

**Test Case: `test_get_student_course_overview_invalid_course_id`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   - **Inputs:**

     .. code-block:: json

       {
         "course_id": "999",
         "student_id": "1"
       }

   - **Expected Output:**

     .. code-block:: json

       {
         "detail": "Enrollment not found"
       }

   - **Actual Output:**

     .. code-block:: json

       {
         "detail": "Enrollment not found"
       }

   - **Result:** Success

**Test Case: `test_get_student_course_overview_invalid_student_id`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   - **Inputs:**

     .. code-block:: json

       {
         "course_id": "1",
         "student_id": "999"
       }

   - **Expected Output:**

     .. code-block:: json

       {
         "detail": "Enrollment not found"
       }

   - **Actual Output:**

     .. code-block:: json

       {
         "detail": "Enrollment not found"
       }

   - **Result:** Success

**Test Case: `test_get_student_course_overview_invalid_ids`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   - **Inputs:**

     .. code-block:: json

       {
         "course_id": "999",
         "student_id": "999"
       }

   - **Expected Output:**

     .. code-block:: json

       {
         "detail": "Enrollment not found"
       }

   - **Actual Output:**

     .. code-block:: json

       {
         "detail": "Enrollment not found"
       }

   - **Result:** Success

**Test Cases for `/student/enrolled_course/`**
--------------------------------------------------

**Test Case: `test_get_module_details_success`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   - **Inputs:**

     .. code-block:: json

       {
         "course_id": "1",
         "module_id": "1"
       }

   - **Expected Output:**

     .. code-block:: json

       {
         "title": "Test Module",
         "total_lectures": 5,
         "total_assignments": 3
       }

   - **Actual Output:**

     .. code-block:: json

       {
         "title": "Test Module",
         "total_lectures": 5,
         "total_assignments": 3
       }

   - **Result:** Success

**Test Case: `test_get_module_details_invalid_course_id`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   - **Inputs:**

     .. code-block:: json

       {
         "course_id": "999",
         "module_id": "1"
       }

   - **Expected Output:**

     .. code-block:: json

       {
         "detail": "Module not found"
       }

   - **Actual Output:**

     .. code-block:: json

       {
         "detail": "Module not found"
       }

   - **Result:** Success

**Test Case: `test_get_module_details_invalid_module_id`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   - **Inputs:**

     .. code-block:: json

       {
         "course_id": "1",
         "module_id": "999"
       }

   - **Expected Output:**

     .. code-block:: json

       {
         "detail": "Module not found"
       }

   - **Actual Output:**

     .. code-block:: json

       {
         "detail": "Module not found"
       }

   - **Result:** Success

**Test Case: `test_get_module_details_invalid_ids`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   - **Inputs:**

     .. code-block:: json

       {
         "course_id": "999",
         "module_id": "999"
       }

   - **Expected Output:**

     .. code-block:: json

       {
         "detail": "Module not found"
       }

   - **Actual Output:**

     .. code-block:: json

       {
         "detail": "Module not found"
       }

   - **Result:** Success

**Test Cases for `/student/courses/{course_id}`**
-----------------------------------------------------

**Test Case: `test_get_course_details_success`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   - **Inputs:** None

   - **Expected Output:**

     .. code-block:: json

       {
         "title": "Test Course",
         "description": "Test Description",
         "total_modules": 10,
         "price": 100.0
       }

   - **Actual Output:**

     .. code-block:: json

       {
         "title": "Test Course",
         "description": "Test Description",
         "total_modules": 10,
         "price": 100.0
       }

   - **Result:** Success

**Test Case: `test_get_course_details_invalid_course_id`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   - **Inputs:** None

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

**Test Cases for `/student/enroll`**
--------------------------------------

**Test Case: `test_enroll_student_success`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   - **Inputs:**

     .. code-block:: json

       {
         "student_id": "1",
         "course_id": "2"
       }

   - **Expected Output:**

     .. code-block:: json

       {
         "message": "Enrollment successful"
       }

   - **Actual Output:**

     .. code-block:: json

       {
         "message": "Enrollment successful"
       }

   - **Result:** Success

**Test Case: `test_enroll_student_invalid_student_id`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   - **Inputs:**

     .. code-block:: json

       {
         "student_id": "999",
         "course_id": "1"
       }

   - **Expected Output:**

     .. code-block:: json

       {
         "detail": "Student or Course not found"
       }

   - **Actual Output:**

     .. code-block:: json

       {
         "detail": "Student or Course not found"
       }

   - **Result:** Success

**Test Case: `test_enroll_student_invalid_course_id`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   - **Inputs:**

     .. code-block:: json

       {
         "student_id": "1",
         "course_id": "999"
       }

   - **Expected Output:**

     .. code-block:: json

       {
         "detail": "Student or Course not found"
       }

   - **Actual Output:**

     .. code-block:: json

       {
         "detail": "Student or Course not found"
       }

   - **Result:** Success

**Test Cases for `/student/enrolled-courses/{student_id}`**
----------------------------------------------------------------

**Test Case: `test_get_enrolled_courses_success`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   - **Inputs:** None

   - **Expected Output:**

     .. code-block:: json

       [
         {
           "id": 1,
           "title": "Test Course"
         }
       ]

   - **Actual Output:**

     .. code-block:: json

       [
         {
           "id": 1,
           "title": "Test Course"
         }
       ]

   - **Result:** Success

**Test Case: `test_get_enrolled_courses_invalid_student_id`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   - **Inputs:** None

   - **Expected Output:**

     .. code-block:: json

       []

   - **Actual Output:**

     .. code-block:: json

       []

   - **Result:** Success

**Test Case: `test_get_enrolled_courses_no_courses`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   - **Inputs:** None

   - **Expected Output:**

     .. code-block:: json

       []

   - **Actual Output:**

     .. code-block:: json

       []

   - **Result:** Success
