import pytest
import os
from pathlib import Path


@pytest.fixture
def css_file_path():
    return Path("static/css/style.css")


def test_css_file_exists(css_file_path):
    assert css_file_path.exists(), f"CSS file not found at {css_file_path}"


def test_css_file_non_empty(css_file_path):
    assert css_file_path.stat().st_size > 0, f"CSS file at {css_file_path} is empty"


def test_css_file_contains_css_variables(css_file_path):
    content = css_file_path.read_text()
    assert ":root" in content or "var(" in content, "CSS file must define CSS variables (e.g., using :root or var())"


def test_css_file_contains_expected_design_system_properties(css_file_path):
    content = css_file_path.read_text()
    required_properties = ["color", "font-size", "margin", "padding"]
    found_any = any(prop in content for prop in required_properties)
    assert found_any, f"CSS file must contain at least one of the expected design system properties: {required_properties}"


def test_css_file_syntax_valid_basic(css_file_path):
    content = css_file_path.read_text()
    # Basic sanity check: balanced braces
    assert content.count("{") == content.count("}"), "CSS file has unbalanced braces"
    assert content.count("(") == content.count(")"), "CSS file has unbalanced parentheses in var() or similar"