import pytest
from unittest.mock import MagicMock, patch
from fastapi import FastAPI
from fastapi.testclient import TestClient

# Import only what's expected to be public in src/main.py
from src.main import app, api_router


@pytest.fixture
def client():
    return TestClient(app)


def test_app_exists():
    assert app is not None
    assert isinstance(app, FastAPI)


def test_api_router_exists():
    assert api_router is not None


@patch("src.main.api_router")
def test_app_includes_router(mock_router):
    # Ensure router is attached (if app.include_router is called during app creation)
    # We're not patching app.include_router directly because we don't control app creation timing
    # Instead, we verify the router is attached by inspecting routes
    route_paths = [route.path for route in app.routes if hasattr(route, "path")]
    # Assuming api_router has at least one path like /api/*
    assert any("/api" in path for path in route_paths)


def test_health_endpoint(client):
    with patch("src.main.api_router") as mock_router:
        # Mock any dependencies if needed, but health endpoint is usually simple
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}  # adjust to actual contract


def test_docs_endpoint_exists(client):
    # FastAPI includes /docs and /openapi.json by default
    response = client.get("/docs")
    assert response.status_code == 200
    assert "swagger-ui" in response.text.lower() or "redoc" in response.text.lower()


def test_openapi_schema_exists(client):
    response = client.get("/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    assert "openapi" in schema
    assert "paths" in schema
    assert isinstance(schema["paths"], dict)