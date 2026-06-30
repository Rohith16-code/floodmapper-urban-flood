import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_app_exists():
    assert app is not None
    assert isinstance(app, FastAPI)


def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "real-time-urban-flood-inundation-mapping" in response.text.lower()


def test_dashboard_endpoint(client):
    response = client.get("/dashboard")
    assert response.status_code == 200
    assert "<title>" in response.text


def test_static_files_exist(client):
    response = client.get("/static/css/style.css")
    assert response.status_code == 200
    response = client.get("/static/js/app.js")
    assert response.status_code == 200


def test_docs_endpoint_exists(client):
    response = client.get("/docs")
    assert response.status_code == 200


def test_openapi_schema_exists(client):
    response = client.get("/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    assert "openapi" in schema
    assert "paths" in schema
