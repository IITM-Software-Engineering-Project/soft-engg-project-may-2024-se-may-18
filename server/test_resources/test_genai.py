import pytest
from fastapi.testclient import TestClient
import sys,os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import app  # Import your FastAPI app

client = TestClient(app)

# Test case for /ai-search-courses
def test_ai_search_courses_success():
    response = client.post("/ai-search-courses", json={
        "prompt": "Find courses on data science", # Mock additional data if needed
    })
    assert response.status_code == 200
    
def test_ai_search_courses_no_data():
    response = client.post("/ai-search-courses", json={
        "prompt": "Find courses on data science"
    })
    assert response.status_code == 200
   
def test_ai_search_courses_missing_prompt():
    response = client.post("/ai-search-courses", json={})
    assert response.status_code == 422  # Unprocessable Entity if missing required field

# Test case for /ai-explain-course
def test_ai_explain_course_success():
    response = client.post("/ai-explain-course", json={
        "prompt": "Explain the basics of machine learning",
        # "data": {"additional_data": "value"}  # Mock additional data if needed
    })
    assert response.status_code == 200
    

def test_ai_explain_course_no_data():
    response = client.post("/ai-explain-course", json={
        "prompt": "Explain the basics of machine learning"
    })
    assert response.status_code == 200
    
def test_ai_explain_course_missing_prompt():
    response = client.post("/ai-explain-course", json={})
    assert response.status_code == 422  # Unprocessable Entity if missing required field

# Test case for /ai-summarize-transcript
def test_ai_summarize_transcript_success():
    response = client.post("/ai-summarize-transcript", json={
        "prompt": "Summarize the transcript of the lecture on AI",
        "data": "Transcript data here"  # Mock transcript data if needed
    })
    assert response.status_code == 200
    

def test_ai_summarize_transcript_no_data():
    response = client.post("/ai-summarize-transcript", json={
        "prompt": "Summarize the transcript of the lecture on AI"
    })
    assert response.status_code == 200
    
def test_ai_summarize_transcript_missing_prompt():
    response = client.post("/ai-summarize-transcript", json={})
    assert response.status_code == 422  # Unprocessable Entity if missing required field

# Test case for /ai-programming-feedback
def test_ai_programming_feedback_success():
    # Mocking file upload
    files = [
        ('images', ('test_image.png', open('test_image.png', 'rb'), 'image/png'))
    ]
    response = client.post("/ai-programming-feedback", files=files, data={
        "prompt": "Provide feedback on this code",
        "data": "Code snippet here",  # Mock code data if needed
        "language": "Python",
        "question": "How can I optimize this code?"
    })
    assert response.status_code == 200

def test_ai_programming_feedback_missing_data():
    # Mocking file upload
    files = [
        ('images', ('test_image.png', open('test_image.png', 'rb'), 'image/png'))
    ]
    response = client.post("/ai-programming-feedback", files=files, data={
        "prompt": "Provide feedback on this code",
        "language": "Python",
        "question": "How can I optimize this code?"
    })
    assert response.status_code == 200

def test_ai_programming_feedback_missing_prompt():
    # Mocking file upload
    files = [
        ('images', ('test_image.png', open('test_image.png', 'rb'), 'image/png'))
    ]
    response = client.post("/ai-programming-feedback", files=files, data={
        "data": "Code snippet here",
        "language": "Python",
        "question": "How can I optimize this code?"
    })
    assert response.status_code == 200  
