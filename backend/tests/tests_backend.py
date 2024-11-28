import pytest

def test_app_initialization():
    try:
        # Try importing the app and ensuring it doesn't throw any errors
        import backend.app  # Ensure this path matches the actual path of your app.py
    except Exception as e:
        pytest.fail(f"App failed to initialize with error: {e}")
