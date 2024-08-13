Instructor API Test Cases
============================

This document provides details about the unit tests for the API endpoints related to intructor course management. Each test case includes information about the API being tested, the inputs, expected output, actual output, and the result.

**Test Cases for `/add_module`**
---------------------------------------

**Test Case: `test_add_module_success`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   - **API being tested:** `/add_module`
   - **Inputs:**

     .. code-block:: json

       {
         "title": "New Module",
         "description": "Module Description",
         "total_lectures": 6,
         "course_id": 1
       }

   - **Expected Output:**

     .. code-block:: json

       {
         "message": "Module added successfully"
       }

   - **Actual Output:**
   
     .. code-block:: json

       {
         "message": "Module added successfully"
       }

   - **Result:** Success


**Test Case: `test_add_module_invalid_courseid`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   - **API being tested:** `/add_module`
   - **Inputs:**

     .. code-block:: json

       {
         "title": "New Module",
         "description": "Module Description",
         "total_lectures": 6,
         "course_id": 2
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


**Test Cases for `/edit_module`**
----------------------------------------

**Test Case: `test_edit_module_success`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   - **API being tested:** `/edit_module/1`
   - **Inputs:**

     .. code-block:: json

       {
         "title": "Updated Module Title"
       }

   - **Expected Output:**

     .. code-block:: json

       {
         "message": "Module updated successfully"
       }

   - **Actual Output:** 

     .. code-block:: json

       {
         "message": "Module updated successfully"
       }

   - **Result:** Success


**Test Case: `test_edit_module_not_found`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   - **API being tested:** `/edit_module/999`
   - **Inputs:**

     .. code-block:: json

       {
         "title": "Updated Module Title"
       }

   - **Expected Output:**

     .. code-block:: json

       {
         "detail": "Content not found"
       }

   - **Actual Output:** 

     .. code-block:: json

       {
         "detail": "Content not found"
       }

   - **Result:** Success


**Test Cases for `/delete_module`**
------------------------------------------

**Test Case: `test_delete_module_success`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   - **API being tested:** `/delete_module/1`
   - **Inputs:** None

   - **Expected Output:**

     .. code-block:: json

       {
         "message": "Module deleted successfully"
       }

   - **Actual Output:** 

     .. code-block:: json

       {
         "message": "Module deleted successfully"
       }


   - **Result:** Success


**Test Case: `test_delete_module_not_found`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   - **API being tested:** `/delete_module/999`
   - **Inputs:** None

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


**Test Cases for `/add_lecture`**
---------------------------------------

**Test Case: `test_add_lecture_success`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   - **API being tested:** `/add_lecture`
   - **Inputs:**

     .. code-block:: json

       {
         "title": "New Lecture",
         "module_id": 1,
         "url": "http://example.com",
         "transcript": "Lecture Transcript"
       }

   - **Expected Output:**

     .. code-block:: json

       {
         "message": "Lecture added successfully"
       }

   - **Actual Output:** 

     .. code-block:: json

       {
         "message": "Lecture added successfully"
       }

   - **Result:** Success


**Test Case: `test_add_lecture_invalid_moduleid`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   - **API being tested:** `/add_lecture`
   - **Inputs:**

     .. code-block:: json

       {
         "title": "New Lecture",
         "module_id": 999,
         "url": "http://example.com",
         "transcript": "Lecture Transcript"
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


**Test Cases for `/edit_lecture`**
----------------------------------------

**Test Case: `test_edit_lecture_success`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   - **API being tested:** `/edit_lecture/1`
   - **Inputs:**

     .. code-block:: json

       {
         "title": "Updated Lecture Title"
       }

   - **Expected Output:**

     .. code-block:: json

       {
         "message": "Lecture updated successfully"
       }

   - **Actual Output:** 

     .. code-block:: json

       {
         "message": "Lecture updated successfully"
       }

   - **Result:** Success


**Test Case: `test_edit_lecture_not_found`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   - **API being tested:** `/edit_lecture/999`
   - **Inputs:**

     .. code-block:: json

       {
         "title": "Updated Lecture Title"
       }

   - **Expected Output:**

     .. code-block:: json

       {
         "detail": "Lecture not found"
       }

   - **Actual Output:** 

     .. code-block:: json

       {
         "detail": "Lecture not found"
       }

   - **Result:** Success


**Test Cases for `/delete_lecture`**
------------------------------------------

**Test Case: `test_delete_lecture_success`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   - **API being tested:** `/delete_lecture/1`
   - **Inputs:** None

   - **Expected Output:**

     .. code-block:: json

       {
         "message": "Lecture deleted successfully"
       }

   - **Actual Output:** 

     .. code-block:: json

       {
         "message": "Lecture deleted successfully"
       }

   - **Result:** Success


**Test Case: `test_delete_lecture_not_found`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   - **API being tested:** `/delete_lecture/999`
   - **Inputs:** None

   - **Expected Output:**

     .. code-block:: json

       {
         "detail": "Lecture not found"
       }

   - **Actual Output:** 

     .. code-block:: json

       {
         "detail": "Lecture not found"
       }

   - **Result:** Success


**Test Cases for `/add_assignment`**
-----------------------------------------

**Test Case: `test_add_assignment_success`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   - **API being tested:** `/add_assignment`
   - **Inputs:**

     .. code-block:: json

       {
         "id": 2,
         "title": "New Assignment",
         "description": "Assignment Description",
         "module_id": 1,
         "type": "homework",
         "due_date": "2024-08-05 00:00:00"
       }

   - **Expected Output:**

     .. code-block:: json

       {
         "message": "Assignment added successfully"
       }

   - **Actual Output:** 

     .. code-block:: json

       {
         "message": "Assignment added successfully"
       }

   - **Result:** Success


**Test Case: `test_add_assignment_invalid_moduleid`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   - **API being tested:** `/add_assignment`
   - **Inputs:**

     .. code-block:: json

       {
         "id": 2,
         "title": "New Assignment",
         "description": "Assignment Description",
         "module_id": 999,
         "type": "homework",
         "due_date": "2024-08-05 00:00:00"
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


**Test Cases for `/edit_assignment`**
--------------------------------------------

**Test Case: `test_edit_assignment_success`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   - **API being tested:** `/edit_assignment/1`
   - **Inputs:**

     .. code-block:: json

       {
         "title": "Updated Assignment Title"
       }

   - **Expected Output:**

     .. code-block:: json

       {
         "message": "Assignment updated successfully"
       }

   - **Actual Output:** 

     .. code-block:: json

       {
         "message": "Assignment updated successfully"
       }

   - **Result:** Success


**Test Case: `test_edit_assignment_not_found`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   - **API being tested:** `/edit_assignment/999`
   - **Inputs:**

     .. code-block:: json

       {
         "title": "Updated Assignment Title"
       }

   - **Expected Output:**

     .. code-block:: json

       {
         "detail": "Assignment not found"
       }

   - **Actual Output:** 

     .. code-block:: json

       {
         "detail": "Assignment not found"
       }

   - **Result:** Success


**Test Case: `test_edit_assignment_invalid_moduleid`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   - **API being tested:** `/edit_assignment/1`
   - **Inputs:**

     .. code-block:: json

       {
         "module_id": 999
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


**Test Cases for `/delete_assignment`**
----------------------------------------------

**Test Case: `test_delete_assignment_success`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   - **API being tested:** `/delete_assignment/1`
   - **Inputs:** None

   - **Expected Output:**

     .. code-block:: json

       {
         "message": "Assignment deleted successfully"
       }

   - **Actual Output:** 

     .. code-block:: json

       {
         "message": "Assignment deleted successfully"
       }

   - **Result:** Success


**Test Case: `test_delete_assignment_not_found`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   - **API being tested:** `/delete_assignment/999`
   - **Inputs:** None

   - **Expected Output:**

     .. code-block:: json

       {
         "detail": "Assignment not found"
       }

   - **Actual Output:** 

     .. code-block:: json

       {
         "detail": "Assignment not found"
       }


   - **Result:** Success

**Test Cases for `/add_module`**
---------------------------------------

**Test Case: `test_add_module_success`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   - **API being tested:** `/add_module`
   - **Inputs:**

     .. code-block:: json

       {
         "title": "New Module",
         "description": "Module Description",
         "total_lectures": 6,
         "course_id": 1
       }

   - **Expected Output:**

     .. code-block:: json

       {
         "message": "Module added successfully"
       }

   - **Actual Output:** 

     .. code-block:: json

       {
         "message": "Module added successfully"
       }

   - **Result:** Success


**Test Case: `test_add_module_invalid_courseid`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   - **API being tested:** `/add_module`
   - **Inputs:**

     .. code-block:: json

       {
         "title": "New Module",
         "description": "Module Description",
         "total_lectures": 6,
         "course_id": 2
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


**Test Cases for `/edit_module`**
----------------------------------------

**Test Case: `test_edit_module_success`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   - **API being tested:** `/edit_module/1`
   - **Inputs:**

     .. code-block:: json

       {
         "title": "Updated Module Title"
       }

   - **Expected Output:**

     .. code-block:: json

       {
         "message": "Module updated successfully"
       }

   - **Actual Output:** 

     .. code-block:: json

       {
         "message": "Module updated successfully"
       }


   - **Result:** Success


**Test Case: `test_edit_module_not_found`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   - **API being tested:** `/edit_module/999`
   - **Inputs:**

     .. code-block:: json

       {
         "title": "Updated Module Title"
       }

   - **Expected Output:**

     .. code-block:: json

       {
         "detail": "Content not found"
       }

   - **Actual Output:** 

     .. code-block:: json

       {
         "detail": "Content not found"
       }


   - **Result:** Success


**Test Cases for `/delete_module`**
------------------------------------------

**Test Case: `test_delete_module_success`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   - **API being tested:** `/delete_module/1`
   - **Inputs:** None

   - **Expected Output:**

     .. code-block:: json

       {
         "message": "Module deleted successfully"
       }

   - **Actual Output:** 

     .. code-block:: json

       {
         "message": "Module deleted successfully"
       }

   - **Result:** Success


**Test Case: `test_delete_module_not_found`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   - **API being tested:** `/delete_module/999`
   - **Inputs:** None

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


**Test Cases for `/add_lecture`**
----------------------------------------

**Test Case: `test_add_lecture_success`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   - **API being tested:** `/add_lecture`
   - **Inputs:**

     .. code-block:: json

       {
         "title": "New Lecture",
         "module_id": 1,
         "url": "http://example.com",
         "transcript": "Lecture Transcript"
       }

   - **Expected Output:**

     .. code-block:: json

       {
         "message": "Lecture added successfully"
       }

   - **Actual Output:** 

     .. code-block:: json

       {
         "message": "Lecture added successfully"
       }

   - **Result:** Success


**Test Case: `test_add_lecture_invalid_moduleid`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   - **API being tested:** `/add_lecture`
   - **Inputs:**

     .. code-block:: json

       {
         "title": "New Lecture",
         "module_id": 999,
         "url": "http://example.com",
         "transcript": "Lecture Transcript"
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


**Test Cases for `/edit_lecture`**
-----------------------------------------

**Test Case: `test_edit_lecture_success`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   - **API being tested:** `/edit_lecture/1`
   - **Inputs:**

     .. code-block:: json

       {
         "title": "Updated Lecture Title"
       }

   - **Expected Output:**

     .. code-block:: json

       {
         "message": "Lecture updated successfully"
       }

   - **Actual Output:** 

     .. code-block:: json

       {
         "message": "Lecture updated successfully"
       }

   - **Result:** Success


**Test Case: `test_edit_lecture_not_found`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   - **API being tested:** `/edit_lecture/999`
   - **Inputs:**

     .. code-block:: json

       {
         "title": "Updated Lecture Title"
       }

   - **Expected Output:**

     .. code-block:: json

       {
         "detail": "Lecture not found"
       }

   - **Actual Output:** 

     .. code-block:: json

       {
         "detail": "Lecture not found"
       }
   - **Result:** Success


**Test Cases for `/delete_lecture`**
-------------------------------------------

**Test Case: `test_delete_lecture_success`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   - **API being tested:** `/delete_lecture/1`
   - **Inputs:** None

   - **Expected Output:**

     .. code-block:: json

       {
         "message": "Lecture deleted successfully"
       }

   - **Actual Output:** 

     .. code-block:: json

       {
         "message": "Lecture deleted successfully"
       }

   - **Result:** Success


**Test Case: `test_delete_lecture_not_found`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   - **API being tested:** `/delete_lecture/999`
   - **Inputs:** None

   - **Expected Output:**

     .. code-block:: json

       {
         "detail": "Lecture not found"
       }

   - **Actual Output:** 

     .. code-block:: json

       {
         "detail": "Lecture not found"
       }

   - **Result:** Success


**Test Cases for `/add_assignment`**
--------------------------------------------

**Test Case: `test_add_assignment_success`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   - **API being tested:** `/add_assignment`
   - **Inputs:**

     .. code-block:: json

       {
         "id": 2,
         "title": "New Assignment",
         "description": "Assignment Description",
         "module_id": 1,
         "type": "homework",
         "due_date": "2024-08-05 00:00:00"
       }

   - **Expected Output:**

     .. code-block:: json

       {
         "message": "Assignment added successfully"
       }

   - **Actual Output:** 

     .. code-block:: json

       {
         "message": "Assignment added successfully"
       }


   - **Result:** Success


**Test Case: `test_add_assignment_invalid_moduleid`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   - **API being tested:** `/add_assignment`
   - **Inputs:**

     .. code-block:: json

       {
         "id": 2,
         "title": "New Assignment",
         "description": "Assignment Description",
         "module_id": 999,
         "type": "homework",
         "due_date": "2024-08-05 00:00:00"
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


**Test Cases for `/edit_assignment`**
--------------------------------------------

**Test Case: `test_edit_assignment_success`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   - **API being tested:** `/edit_assignment/1`
   - **Inputs:**

     .. code-block:: json

       {
         "title": "Updated Assignment Title"
       }

   - **Expected Output:**

     .. code-block:: json

       {
         "message": "Assignment updated successfully"
       }

   - **Actual Output:** 

     .. code-block:: json

       {
         "message": "Assignment updated successfully"
       }

   - **Result:** Success


**Test Case: `test_edit_assignment_not_found`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   - **API being tested:** `/edit_assignment/999`
   - **Inputs:**

     .. code-block:: json

       {
         "title": "Updated Assignment Title"
       }

   - **Expected Output:**

     .. code-block:: json

       {
         "detail": "Assignment not found"
       }

   - **Actual Output:** 

     .. code-block:: json

       {
         "detail": "Assignment not found"
       }

   - **Result:** Success


**Test Case: `test_edit_assignment_invalid_moduleid`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   - **API being tested:** `/edit_assignment/1`
   - **Inputs:**

     .. code-block:: json

       {
         "module_id": 999
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


**Test Cases for `/delete_assignment`**
-----------------------------------------------

**Test Case: `test_delete_assignment_success`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   - **API being tested:** `/delete_assignment/1`
   - **Inputs:** None

   - **Expected Output:**

     .. code-block:: json

       {
         "message": "Assignment deleted successfully"
       }

   - **Actual Output:** 

     .. code-block:: json

       {
         "message": "Assignment deleted successfully"
       }

   - **Result:** Success


**Test Case: `test_delete_assignment_not_found`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   - **API being tested:** `/delete_assignment/999`
   - **Inputs:** None

   - **Expected Output:**

     .. code-block:: json

       {
         "detail": "Assignment not found"
       }

   - **Actual Output:** 

     .. code-block:: json

       {
         "detail": "Assignment not found"
       }

   - **Result:** Success
