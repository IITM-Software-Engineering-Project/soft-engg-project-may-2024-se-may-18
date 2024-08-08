Authentication API Test Cases
=============================

This document provides details about the unit tests for the authentication API endpoints. Each test case includes information about the API being tested, the inputs, expected output, actual output, and the result.

**Test Cases for `/register`**
--------------------------------------

**Test Case: `test_register_success`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **API being tested:** `/register`

- **Inputs:**

  .. code-block:: json

    {
      "username": "testuser",
      "email": "testuser@example.com",
      "password": "password123",
      "role": "user"
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

**Test Case: `test_register_existing_user`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **API being tested:** `/register`

- **Inputs:**

  .. code-block:: json

    {
      "username": "testuser",
      "email": "testuser@example.com",
      "password": "password123",
      "role": "user"
    }

  .. code-block:: json

    {
      "username": "testuser",
      "email": "newemail@example.com",
      "password": "newpassword123",
      "role": "user"
    }

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

**Test Case: `test_register_missing_fields`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **API being tested:** `/register`

- **Inputs:**

  .. code-block:: json

    {
      "username": "testuser",
      "email": "testuser@example.com"
    }

- **Expected Output:**

  .. code-block:: json

    {
      "detail": "Field required"
    }

- **Actual Output:**

  .. code-block:: json

    {
      "detail": "Field required"
    }

- **Result:** Success

**Test Cases for `/login`**
-----------------------------------

**Test Case: `test_login_success`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **API being tested:** `/login`

- **Inputs:**

  .. code-block:: json

    {
      "username": "testuser",
      "password": "password123"
    }

- **Expected Output:**

  .. code-block:: json

    {
      "access_token": "string",
      "username": "testuser",
      "role": "user",
      "email": "testuser@example.com"
    }

- **Actual Output:**

  .. code-block:: json

    {
      "access_token": "string",
      "username": "testuser",
      "role": "user",
      "email": "testuser@example.com"
    }

- **Result:** Success

**Test Case: `test_login_incorrect_password`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **API being tested:** `/login`

- **Inputs:**

  .. code-block:: json

    {
      "username": "testuser",
      "password": "wrongpassword"
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

**Test Case: `test_login_non_existing_user`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **API being tested:** `/login`

- **Inputs:**

  .. code-block:: json

    {
      "username": "nonexistentuser",
      "password": "password123"
    }

- **Expected Output:**

  .. code-block:: json

    {
      "detail": "User does not exist"
    }

- **Actual Output:**

  .. code-block:: json

    {
      "detail": "User does not exist"
    }

- **Result:** Success

**Test Cases for `/verify-token`**
-----------------------------------

**Test Case: `test_verify_token_success`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **API being tested:** `/verify-token`

- **Inputs:**

  .. code-block:: json

    {
      "Authorization": "Bearer validtoken"
    }

- **Expected Output:**

  .. code-block:: json

    {
      "username": "testuser",
      "role": "user",
      "email": "testuser@example.com"
    }

- **Actual Output:**

  .. code-block:: json

    {
      "username": "testuser",
      "role": "user",
      "email": "testuser@example.com"
    }

- **Result:** Success

**Test Case: `test_verify_token_invalid`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **API being tested:** `/verify-token`

- **Inputs:**

  .. code-block:: json

    {
      "Authorization": "Bearer invalidtoken"
    }

- **Expected Output:**

  .. code-block:: json

    {
      "detail": "Invalid token"
    }

- **Actual Output:**

  .. code-block:: json

    {
      "detail": "Invalid token"
    }

- **Result:** Success






