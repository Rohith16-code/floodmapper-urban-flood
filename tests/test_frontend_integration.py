import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_health_endpoint_returns_valid_schema():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert isinstance(data["status"], str)

def test_dashboard_page_loads_and_contains_required_assets():
    response = client.get("/dashboard")
    assert response.status_code == 200
    html = response.text
    assert "/static/css/style.css" in html
    assert "/static/js/app.js" in html

def test_static_index_html_returns_200():
    response = client.get("/static/index.html")
    assert response.status_code == 200