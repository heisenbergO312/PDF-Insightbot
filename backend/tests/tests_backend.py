import os
import pytest
from fastapi.testclient import TestClient
from backend.app import app

# Create a temporary directory for storing test PDFs
TEMP_DIR = "backend/tests/temp"

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as client:
        yield client

@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown():
    # Setup: Create a temporary directory for the test PDFs
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)
    
    # Create a dummy PDF file for testing purposes
    test_pdf_path = os.path.join(TEMP_DIR, "test_file.pdf")
    with open(test_pdf_path, "wb") as f:
        f.write(b"%PDF-1.4 dummy pdf content")
    
    yield
    
    # Teardown: Clean up the temporary files after the tests
    if os.path.exists(TEMP_DIR):
        for file in os.listdir(TEMP_DIR):
            os.remove(os.path.join(TEMP_DIR, file))
        os.rmdir(TEMP_DIR)

def test_upload(client):
    # Test the /upload endpoint
    with open(os.path.join(TEMP_DIR, "test_file.pdf"), "rb") as file:
        response = client.post("/upload", files={"file": ("test_file.pdf", file, "application/pdf")})
    
    assert response.status_code == 200
    assert "PDF file uploaded and saved successfully" in response.json()["message"]

def test_chat(client):
    # Test the /chat endpoint
    file_path = os.path.join(TEMP_DIR, "test_file.pdf")  # Provide the path where the file is uploaded
    query = "What is this document about?"  # A sample query for testing
    
    response = client.post("/chat", json={"query": query, "file_path": file_path})
    
    assert response.status_code == 200
    assert "result" in response.json()
    assert "conversation_result" in response.json()

