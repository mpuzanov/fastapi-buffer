from fastapi.testclient import TestClient
from backend.buffer.main import app

client = TestClient(app)

def test_simple() -> None:
    """Simple test. Checking pytest."""
    print('Simple test to check pytest.')
    try:
        import backend.buffer
    except ImportError:
        raise AssertionError
    else:
        assert backend.buffer

def test_index():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {"message": "Hello API Buffer Applications!"}        