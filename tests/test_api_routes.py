import pytest
from fastapi.testclient import TestClient
from src.api.routes import router
from src.main import app

# Mount router to app for integration testing
app.include_router(router)


def test_flood_prediction_endpoint_success():
    """Test valid flood prediction request."""
    client = TestClient(app)
    payload = {
        "location_id": "loc_001",
        "timestamp": "2023-10-05T14:30:00Z",
        "rainfall_mm": 45.2,
        "water_level_cm": 120.5
    }
    response = client.post("/api/v1/flood/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "inundation_depth_cm" in data
    assert "risk_level" in data
    assert data["risk_level"] in ["low", "moderate", "high", "critical"]


def test_flood_prediction_endpoint_validation_error():
    """Test request with missing required fields."""
    client = TestClient(app)
    payload = {
        "location_id": "loc_001"
        # missing other required fields
    }
    response = client.post("/api/v1/flood/predict", json=payload)
    assert response.status_code == 422


def test_flood_history_endpoint():
    """Test flood history retrieval."""
    client = TestClient(app)
    response = client.get("/api/v1/flood/history?location_id=loc_001")
    assert response.status_code == 200
    data = response.json()
    assert "history" in data
    assert isinstance(data["history"], list)
