import pytest
from fastapi.testclient import TestClient
from backend.app import app  # Ensure this import is correct, depending on your project structure

@pytest.fixture
def client():
    return TestClient(app)

def test_app_initialization(client):
    # Just check if the app initializes correctly
    try:
        # Check if we can access the root endpoint without running any queries
        response = client.get("/")
        assert response.status_code == 200  # Expecting the root endpoint to work
    except Exception as e:
        pytest.fail(f"App initialization failed with error: {e}")

def test_upload_endpoint(client):
    # Check if the upload endpoint works without running any queries
    try:
        response = client.post("/upload", files={"file": ("test.pdf", b"sample pdf content")})
        assert response.status_code == 200
        assert "file_path" in response.json()
    except Exception as e:
        pytest.fail(f"Upload endpoint failed with error: {e}")

def test_chat_endpoint(client):
    # Skip running queries and just ensure the chat endpoint compiles and runs
    try:
        response = client.post("/chat", json={"query": "test", "file_path": "test.pdf"})
        # Check that the response is not empty or invalid
        assert response.status_code == 200
    except Exception as e:
        pytest.fail(f"Chat endpoint failed with error: {e}")
