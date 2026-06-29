import pytest
from fastapi.testclient import TestClient
from src.main import app


def test_main_app_exists():
    """Verify the FastAPI app is instantiated."""
    assert app is not None


def test_health_endpoint():
    """Test the health check endpoint."""
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_static_files_mounted():
    """Verify static files are served correctly."""
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "real-time-urban-flood-inundation-mapping" in response.text.lower()
