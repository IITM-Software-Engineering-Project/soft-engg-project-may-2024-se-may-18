Test Cases for Instructor Endpoints
=====================================

This document provides details about the unit tests for the API endpoints related to intructor course management. Each test case includes information about the API being tested, the inputs, expected output, actual output, and the result.

1. **Test Cases for `/add_module`**
---------------------------------------

1.1 **Test Case: `test_add_module_success`**
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


1.2 **Test Case: `test_add_module_invalid_courseid`**
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


2. **Test Cases for `/edit_module`**
----------------------------------------

2.1 **Test Case: `test_edit_module_success`**
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


2.2 **Test Case: `test_edit_module_not_found`**
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


3. **Test Cases for `/delete_module`**
------------------------------------------

3.1 **Test Case: `test_delete_module_success`**
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


3.2 **Test Case: `test_delete_module_not_found`**
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


4. **Test Cases for `/add_lecture`**
---------------------------------------

4.1 **Test Case: `test_add_lecture_success`**
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


4.2 **Test Case: `test_add_lecture_invalid_moduleid`**
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


5. **Test Cases for `/edit_lecture`**
----------------------------------------

5.1 **Test Case: `test_edit_lecture_success`**
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


5.2 **Test Case: `test_edit_lecture_not_found`**
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


6. **Test Cases for `/delete_lecture`**
------------------------------------------

6.1 **Test Case: `test_delete_lecture_success`**
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


6.2 **Test Case: `test_delete_lecture_not_found`**
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


7. **Test Cases for `/add_assignment`**
-----------------------------------------

7.1 **Test Case: `test_add_assignment_success`**
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


7.2 **Test Case: `test_add_assignment_invalid_moduleid`**
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


8. **Test Cases for `/edit_assignment`**
--------------------------------------------

8.1 **Test Case: `test_edit_assignment_success`**
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


8.2 **Test Case: `test_edit_assignment_not_found`**
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


8.3 **Test Case: `test_edit_assignment_invalid_moduleid`**
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


9. **Test Cases for `/delete_assignment`**
----------------------------------------------

9.1 **Test Case: `test_delete_assignment_success`**
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


9.2 **Test Case: `test_delete_assignment_not_found`**
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

10. **Test Cases for `/add_module`**
---------------------------------------

10.1 **Test Case: `test_add_module_success`**
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


10.2 **Test Case: `test_add_module_invalid_courseid`**
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


12. **Test Cases for `/edit_module`**
----------------------------------------

12.1 **Test Case: `test_edit_module_success`**
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


12.2 **Test Case: `test_edit_module_not_found`**
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


13. **Test Cases for `/delete_module`**
------------------------------------------

13.1 **Test Case: `test_delete_module_success`**
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


13.2 **Test Case: `test_delete_module_not_found`**
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


14. **Test Cases for `/add_lecture`**
----------------------------------------

14.1 **Test Case: `test_add_lecture_success`**
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


14.2 **Test Case: `test_add_lecture_invalid_moduleid`**
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


15. **Test Cases for `/edit_lecture`**
-----------------------------------------

15.1 **Test Case: `test_edit_lecture_success`**
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


15.2 **Test Case: `test_edit_lecture_not_found`**
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


16. **Test Cases for `/delete_lecture`**
-------------------------------------------

16.1 **Test Case: `test_delete_lecture_success`**
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


16.2 **Test Case: `test_delete_lecture_not_found`**
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


17. **Test Cases for `/add_assignment`**
--------------------------------------------

17.1 **Test Case: `test_add_assignment_success`**
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


17.2 **Test Case: `test_add_assignment_invalid_moduleid`**
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


18. **Test Cases for `/edit_assignment`**
--------------------------------------------

18.1 **Test Case: `test_edit_assignment_success`**
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


18.2 **Test Case: `test_edit_assignment_not_found`**
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


18.3 **Test Case: `test_edit_assignment_invalid_moduleid`**
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


19. **Test Cases for `/delete_assignment`**
-----------------------------------------------

19.1 **Test Case: `test_delete_assignment_success`**
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


19.2 **Test Case: `test_delete_assignment_not_found`**
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
