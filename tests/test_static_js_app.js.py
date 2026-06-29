import os
import pytest
import re
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
    # Use regex with word boundaries to ensure /api/v1/health is used in actual fetch calls
    # Match fetch calls that contain the endpoint as a string argument
    pattern = r'fetch\s*\(\s*["\']\/api\/v1\/health["\']'
    assert re.search(pattern, content), "app.js must reference /api/v1/health endpoint in a fetch call"


def test_app_js_contains_fetch_calls_with_expected_paths(app_js_path):
    content = app_js_path.read_text()
    # Use regex to ensure /api/v1/health is used in actual fetch calls
    pattern = r'fetch\s*\(\s*["\']\/api\/v1\/health["\']'
    assert re.search(pattern, content), \
        "app.js must reference the required API endpoint /api/v1/health in a fetch call"


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