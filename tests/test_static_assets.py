import os
import re
from pathlib import Path


def test_index_html_exists():
    """Verify index.html exists and is non-empty."""
    path = Path(__file__).parent.parent / 'static' / 'index.html'
    assert path.is_file()
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    assert len(content) > 0
    # Use case-insensitive regex to match variations of the words
    assert re.search(r'\bdashboard\b', content, re.IGNORECASE)
    assert re.search(r'\bflood\b', content, re.IGNORECASE)


def test_css_variables_defined():
    """Verify CSS uses expected design system variables."""
    path = Path(__file__).parent.parent / 'static' / 'css' / 'style.css'
    assert path.is_file()
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    assert ":root" in content
    assert "--primary-color" in content
    assert "--danger-color" in content


def test_js_app_exists_and_has_fetch():
    """Verify frontend JS exists and uses fetch API."""
    path = Path(__file__).parent.parent / 'static' / 'js' / 'app.js'
    assert path.is_file()
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    assert len(content) > 0
    assert "fetch(" in content or "fetch(" in content.replace(" ", "")