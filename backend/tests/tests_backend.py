import os
import pytest
from fastapi.testclient import TestClient
from backend.app import app  # Ensure this import is correct, depending on your project structure

# Fixed path for the test PDF
TEST_PDF_PATH = "/Users/rohan/Developer/PDF-Insightbot/backend/tests/ASAG_NLP.pdf"

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as client:
        yield client

@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown():
    # Setup: Ensure the test PDF exists
    if not os.path.exists(TEST_PDF_PATH):
        os.makedirs(os.path.dirname(TEST_PDF_PATH), exist_ok=True)
        with open(TEST_PDF_PATH, "wb") as f:
            f.write(b"%PDF-1.4 dummy pdf content")
    
    yield
    
    # Teardown: Clean up the test PDF after the tests
    if os.path.exists(TEST_PDF_PATH):
        os.remove(TEST_PDF_PATH)

def test_upload(client):
    print("Running test_upload")
    # Test the /upload endpoint
    with open(TEST_PDF_PATH, "rb") as file:
        response = client.post("/upload", files={"file": ("test_file.pdf", file, "application/pdf")})
    
    assert response.status_code == 200
    assert "PDF file uploaded and saved successfully" in response.json()["message"]

def test_chat(client):
    print("Running test_chat")
    # Test the /chat endpoint
    query = "What is this document about?"  # A sample query for testing
    
    response = client.post("/chat", json={"query": query, "file_path": TEST_PDF_PATH})
    
    assert response.status_code == 200
    assert "result" in response.json()
    assert "conversation_result" in response.json()
