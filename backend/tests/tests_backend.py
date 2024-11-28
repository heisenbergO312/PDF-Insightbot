import os
import pytest
from fastapi.testclient import TestClient
from backend.app import app

# Define the path to the specific test file
TEST_FILE_PATH = "/Users/rohan/Developer/PDF-Insightbot/backend/tests/ASAG_NLP.pdf"

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as client:
        yield client

def test_upload(client):
    # Test the /upload endpoint using the specific file
    with open(TEST_FILE_PATH, "rb") as file:
        response = client.post("/upload", files={"file": ("example_file.pdf", file, "application/pdf")})
    
    assert response.status_code == 200
    assert "PDF file uploaded and saved successfully" in response.json()["message"]

def test_chat(client):
    # Test the /chat endpoint
    query = "What is this document about?"  # A sample query for testing
    
    response = client.post("/chat", json={"query": query, "file_path": TEST_FILE_PATH})
    
    assert response.status_code == 200
    assert "result" in response.json()
    assert "conversation_result" in response.json()
