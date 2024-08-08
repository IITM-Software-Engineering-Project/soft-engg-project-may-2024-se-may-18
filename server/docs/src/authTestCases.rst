Authentication Test Cases
==========================

This document provides details about the unit tests for the authentication-related API endpoints. Each test case includes information about the API being tested, the inputs, expected output, actual output, and the result.

1. **Test Cases for `/register`**
--------------------------------------

1.1 **Test Case: `test_register_success`**
   - **API being tested:** `/register`
   - **Inputs:**

     .. code-block:: json

       {
         "username": "testuser",
         "email": "test@example.com",
         "password": "testpassword",
         "role": "student"
       }

   - **Expected Output:**

     .. code-block:: json

       {
         "message": "User registered successfully"
       }

   - **Actual Output:**

     .. code-block:: json

       {
         "message": "User registered successfully"
       }

   - **Result:** Success

1.2 **Test Case: `test_register_user_already_exists`**
   - **API being tested:** `/register`
   - **Inputs:**

     .. code-block:: json

       {
         "username": "testuser",
         "email": "test@example.com",
         "password": "testpassword",
         "role": "student"
       }

   - **Setup:** Ensure a user with `username: testuser` is already present in the database.
   - **Expected Output:**

     .. code-block:: json

       {
         "detail": "User already exists"
       }

   - **Actual Output:**

     .. code-block:: json

       {
         "detail": "User already exists"
       }

   - **Result:** Success

2. **Test Cases for `/login`**
-----------------------------------

2.1 **Test Case: `test_login_success`**
   - **API being tested:** `/login`
   - **Inputs:**

     .. code-block:: json

       {
         "username": "testuser",
         "password": "testpassword"
       }

   - **Setup:** Ensure a user with `username: testuser` is registered with the provided password.
   - **Expected Output:**

     .. code-block:: json

       {
         "access_token": "<token>",
         "token_type": "bearer"
       }

   - **Actual Output:**

     .. code-block:: json

       {
         "access_token": "<token>",
         "token_type": "bearer"
       }

   - **Result:** Success

2.2 **Test Case: `test_login_incorrect_password`**
   - **API being tested:** `/login`
   - **Inputs:**

     .. code-block:: json

       {
         "username": "testuser",
         "password": "wrongpassword"
       }

   - **Setup:** Ensure a user with `username: testuser` is registered in the database.
   - **Expected Output:**

     .. code-block:: json

       {
         "detail": "Incorrect username or password"
       }

   - **Actual Output:**

     .. code-block:: json

       {
         "detail": "Incorrect username or password"
       }

   - **Result:** Success

2.3 **Test Case: `test_login_user_not_found`**
   - **API being tested:** `/login`
   - **Inputs:**

     .. code-block:: json

       {
         "username": "nonexistentuser",
         "password": "testpassword"
       }

   - **Expected Output:**

     .. code-block:: json

       {
         "detail": "Incorrect username or password"
       }

   - **Actual Output:**

     .. code-block:: json

       {
         "detail": "Incorrect username or password"
       }

   - **Result:** Success
