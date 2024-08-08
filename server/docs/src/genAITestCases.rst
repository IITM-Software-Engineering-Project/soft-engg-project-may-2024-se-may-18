AI Service Test Cases
=======================

This document provides details about the unit tests for the AI-related API endpoints. Each test case includes information about the API being tested, the inputs, expected output, actual output, and the result.

**Test Cases for `/ai-search-courses`**
---------------------------------------------

**Test Case: `test_ai_search_courses_success`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   - **API being tested:** `/ai-search-courses`
   - **Inputs:**

     .. code-block:: json

       {
         "prompt": "Find courses on data science"
       }

   - **Expected Output:**
     - Ensure the response contains relevant course information based on the prompt.

   - **Actual Output:** 
     - (Output will vary due to AI response)

   - **Result:** Success

**Test Case: `test_ai_search_courses_no_data`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   - **API being tested:** `/ai-search-courses`
   - **Inputs:**

     .. code-block:: json

       {
         "prompt": "Find courses on data science"
       }

   - **Expected Output:**
     - Ensure the response is successful even if no additional data is provided.

   - **Actual Output:** 
     - (Output will vary due to AI response)

   - **Result:** Success

**Test Case: `test_ai_search_courses_missing_prompt`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   - **API being tested:** `/ai-search-courses`
   - **Inputs:**

     .. code-block:: json

       {}

   - **Expected Output:**

     .. code-block:: json

       {
         "detail": "Unprocessable Entity"
       }

   - **Actual Output:** 

     .. code-block:: json

       {
         "detail": "Unprocessable Entity"
       }

   - **Result:** Success


**Test Cases for `/ai-explain-course`**
---------------------------------------------

**Test Case: `test_ai_explain_course_success`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   - **API being tested:** `/ai-explain-course`
   - **Inputs:**

     .. code-block:: json

       {
         "prompt": "Explain the basics of machine learning"
       }

   - **Expected Output:**
     - Ensure the response contains a detailed explanation of the basics of machine learning.

   - **Actual Output:** 
     - (Output will vary due to AI response)

   - **Result:** Success

**Test Case: `test_ai_explain_course_no_data`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   - **API being tested:** `/ai-explain-course`
   - **Inputs:**

     .. code-block:: json

       {
         "prompt": "Explain the basics of machine learning"
       }

   - **Expected Output:**
     - Ensure the response is successful even if no additional data is provided.

   - **Actual Output:** 
     - (Output will vary due to AI response)

   - **Result:** Success

**Test Case: `test_ai_explain_course_missing_prompt`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   - **API being tested:** `/ai-explain-course`
   - **Inputs:**

     .. code-block:: json

       {}

   - **Expected Output:**

     .. code-block:: json

       {
         "detail": "Unprocessable Entity"
       }

   - **Actual Output:** 

     .. code-block:: json

       {
         "detail": "Unprocessable Entity"
       }

   - **Result:** Success


**Test Cases for `/ai-summarize-transcript`**
------------------------------------------------------

**Test Case: `test_ai_summarize_transcript_success`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   - **API being tested:** `/ai-summarize-transcript`
   - **Inputs:**

     .. code-block:: json

       {
         "prompt": "Summarize the transcript of the lecture on AI",
         "data": "Transcript data here"
       }

   - **Expected Output:**
     - Ensure the response contains a summary of the provided transcript data.

   - **Actual Output:** 
     - (Output will vary due to AI response)

   - **Result:** Success

**Test Case: `test_ai_summarize_transcript_no_data`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   - **API being tested:** `/ai-summarize-transcript`
   - **Inputs:**

     .. code-block:: json

       {
         "prompt": "Summarize the transcript of the lecture on AI"
       }

   - **Expected Output:**
     - Ensure the response is successful even if no additional data is provided.

   - **Actual Output:** 
     - (Output will vary due to AI response)

   - **Result:** Success

**Test Case: `test_ai_summarize_transcript_missing_prompt`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   - **API being tested:** `/ai-summarize-transcript`
   - **Inputs:**

     .. code-block:: json

       {}

   - **Expected Output:**

     .. code-block:: json

       {
         "detail": "Unprocessable Entity"
       }

   - **Actual Output:** 

     .. code-block:: json

       {
         "detail": "Unprocessable Entity"
       }

   - **Result:** Success


**Test Cases for `/ai-programming-feedback`**
----------------------------------------------------

**Test Case: `test_ai_programming_feedback_success`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   - **API being tested:** `/ai-programming-feedback`
   - **Inputs:**
     - **Files:** 

       .. code-block:: json

         {
           "file": {
             "filename": "test_image.png",
             "content_type": "image/png"
           }
         }

     - **Form Data:**

       .. code-block:: json

         {
           "prompt": "Provide feedback on this code",
           "data": "Code snippet here",
           "language": "Python",
           "question": "How can I optimize this code?"
         }

   - **Expected Output:**
     - Ensure the response contains feedback on the provided code.

   - **Actual Output:** 
     - (Output will vary due to AI response)

   - **Result:** Success

**Test Case: `test_ai_programming_feedback_missing_data`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   - **API being tested:** `/ai-programming-feedback`
   - **Inputs:**
     - **Files:** 

       .. code-block:: json

         {
           "file": {
             "filename": "test_image.png",
             "content_type": "image/png"
           }
         }

     - **Form Data:**

       .. code-block:: json

         {
           "prompt": "Provide feedback on this code",
           "language": "Python",
           "question": "How can I optimize this code?"
         }

   - **Expected Output:**
     - Ensure the response is successful even if some data is missing.

   - **Actual Output:** 
     - (Output will vary due to AI response)

   - **Result:** Success

**Test Case: `test_ai_programming_feedback_missing_prompt`**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   - **API being tested:** `/ai-programming-feedback`
   - **Inputs:**
     - **Files:** 

       .. code-block:: json

         {
           "file": {
             "filename": "test_image.png",
             "content_type": "image/png"
           }
         }

     - **Form Data:**

       .. code-block:: json

         {
           "data": "Code snippet here",
           "language": "Python",
           "question": "How can I optimize this code?"
         }

   - **Expected Output:**
     - Ensure the response is successful even if the prompt is missing.

   - **Actual Output:** 
     - (Output will vary due to AI response)

   - **Result:** Success
