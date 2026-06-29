import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from fastapi import FastAPI
from src.api.routes import router


@pytest.fixture
def client():
    # Ensure router is a FastAPI instance for TestClient compatibility
    if not isinstance(router, FastAPI):
        app = FastAPI()
        app.include_router(router)
        return TestClient(app)
    return TestClient(router)


def test_router_exists():
    assert router is not None


@pytest.mark.parametrize(
    "path, expected_status",
    [
        ("/api/v1/health", 200),
    ],
)
def test_health_endpoint(client, path, expected_status):
    response = client.get(path)
    assert response.status_code == expected_status
    data = response.json()
    assert "status" in data
    assert data["status"] == "ok"


@pytest.mark.parametrize(
    "path, expected_status",
    [
        ("/items", 200),
    ],
)
def test_list_items_endpoint(client, path, expected_status):
    with patch("src.api.routes.get_items", return_value=[{"id": 1, "name": "item1"}]) as mock_get_items:
        response = client.get(path)
        assert response.status_code == expected_status
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["id"] == 1
        assert data[0]["name"] == "item1"
        mock_get_items.assert_called_once()


@pytest.mark.parametrize(
    "path, payload, expected_status",
    [
        ("/items", {"name": "new_item"}, 201),
    ],
)
def test_create_item_endpoint(client, path, payload, expected_status):
    with patch("src.api.routes.create_item", return_value={"id": 2, "name": "new_item"}) as mock_create:
        response = client.post(path, json=payload)
        assert response.status_code == expected_status
        data = response.json()
        assert data["id"] == 2
        assert data["name"] == "new_item"
        mock_create.assert_called_once_with(payload)


def test_create_item_validation_error(client):
    with patch("src.api.routes.create_item") as mock_create:
        response = client.post("/items", json={})
        assert response.status_code == 422
        mock_create.assert_not_called()


@pytest.mark.parametrize(
    "item_id, expected_status",
    [
        (1, 200),
        (999, 404),
    ],
)
def test_get_item_endpoint(client, item_id, expected_status):
    with patch("src.api.routes.get_item_by_id") as mock_get_item:
        if item_id == 1:
            mock_get_item.return_value = {"id": 1, "name": "item1"}
        else:
            mock_get_item.side_effect = ValueError("Item not found")

        response = client.get(f"/items/{item_id}")
        assert response.status_code == expected_status

        if expected_status == 200:
            data = response.json()
            assert data["id"] == 1
            assert data["name"] == "item1"
        else:
            data = response.json()
            assert "detail" in data
            assert "not found" in data["detail"].lower() or "Item not found" in str(data.get("detail", ""))