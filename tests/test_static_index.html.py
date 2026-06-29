import pytest
import os
from pathlib import Path
from html.parser import HTMLParser


class IndexHTMLParser(HTMLParser):
    """Simple HTML parser to extract key elements from static/index.html"""
    def __init__(self):
        super().__init__()
        self.title = None
        self.has_main = False
        self.css_links = []
        self.js_links = []
        self.api_endpoints = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == "title" and self.title is None:
            self.title = ""
        elif tag == "main":
            self.has_main = True
        elif tag == "link" and attrs_dict.get("rel") == "stylesheet":
            href = attrs_dict.get("href", "")
            if href.startswith("/static/css/style.css"):
                self.css_links.append(href)
        elif tag == "script" and attrs_dict.get("src"):
            src = attrs_dict.get("src", "")
            if src.startswith("/static/js/app.js"):
                self.js_links.append(src)


@pytest.fixture
def index_html_path():
    """Return path to static/index.html"""
    path = Path("static/index.html")
    assert path.exists(), "static/index.html not found"
    return path


@pytest.fixture
def index_html_content(index_html_path):
    """Read and return content of static/index.html"""
    content = index_html_path.read_text(encoding="utf-8")
    assert len(content) > 0, "static/index.html is empty"
    return content


def test_index_html_exists_and_non_empty(index_html_path):
    """Verify static/index.html exists and is non-empty"""
    assert index_html_path.exists()
    assert index_html_path.stat().st_size > 0


def test_index_html_contains_required_structure(index_html_content):
    """Parse HTML and assert presence of required structural elements"""
    parser = IndexHTMLParser()
    parser.feed(index_html_content)

    assert parser.title is not None, "<title> element missing"
    assert parser.has_main, "<main> element missing"
    assert len(parser.css_links) > 0, "Missing link to /static/css/style.css"
    assert len(parser.js_links) > 0, "Missing script src='/static/js/app.js'"


def test_index_html_contains_api_endpoints(index_html_content):
    """Assert that any referenced backend endpoints from API contracts exist as text in the file"""
    # Define expected API endpoints according to the actual API contract
    expected_endpoints = [
        "/api/v1/health"
    ]

    # Check each endpoint appears as a quoted string in the HTML
    for endpoint in expected_endpoints:
        assert f'"{endpoint}"' in index_html_content or f"'{endpoint}'" in index_html_content, \
            f"Expected API endpoint '{endpoint}' not found in static/index.html"