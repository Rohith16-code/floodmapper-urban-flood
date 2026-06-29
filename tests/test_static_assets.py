import os
from pathlib import Path


def test_index_html_exists():
    """Verify index.html exists and is non-empty."""
    path = Path("static") / "index.html"
    assert os.path.isfile(path)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    assert len(content) > 0
    assert "dashboard" in content.lower()
    assert "flood" in content.lower()


def test_css_variables_defined():
    """Verify CSS uses expected design system variables."""
    path = Path("static") / "css" / "style.css"
    assert os.path.isfile(path)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    assert ":root" in content
    assert "--primary-color" in content
    assert "--danger-color" in content


def test_js_app_exists_and_has_fetch():
    """Verify frontend JS exists and uses fetch API."""
    path = Path("static") / "js" / "app.js"
    assert os.path.isfile(path)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    assert len(content) > 0
    assert "fetch(" in content or "fetch(" in content.replace(" ", "")