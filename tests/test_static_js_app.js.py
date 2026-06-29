import os
import pytest
from pathlib import Path


@pytest.fixture
def app_js_path():
    return Path("static/js/app.js")


def test_app_js_file_exists_and_non_empty(app_js_path):
    assert app_js_path.exists(), f"File {app_js_path} does not exist"
    assert app_js_path.is_file(), f"{app_js_path} is not a file"
    assert app_js_path.stat().st_size > 0, f"File {app_js_path} is empty"


def test_app_js_contains_expected_api_endpoints(app_js_path):
    content = app_js_path.read_text()
    assert "fetch" in content, "app.js must use fetch for API calls"
    # Assert presence of the exact required endpoint per API contract
    assert "/api/v1/health" in content, "app.js must reference /api/v1/health endpoint"


def test_app_js_contains_fetch_calls_with_expected_paths(app_js_path):
    content = app_js_path.read_text()
    # Example: if app.js is expected to call /api/items and /api/health
    # Adjust endpoints to match actual contract
    assert "/api/items" in content or "/api/health" in content, \
        "app.js must reference at least one expected API endpoint"


def test_app_js_exports_or_defines_expected_functions(app_js_path):
    content = app_js_path.read_text()
    # Look for common patterns: function declarations, arrow functions, or module exports
    # Since this is static JS, we only check for structural presence—not execution
    assert any(
        pattern in content
        for pattern in [
            "function ",
            "const ",
            "let ",
            "var ",
            "export ",
        ]
    ), "app.js must define at least one variable/function"