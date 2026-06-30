"""Entry point with API routes and static frontend mount."""
import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

from src.api import routes

app = FastAPI(title="Real-Time Urban Flood Inundation Mapping", version="1.0.0")

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR.parent / "static"

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
app.include_router(routes.router)


@app.get("/", response_class=HTMLResponse)
def read_root():
    index_path = STATIC_DIR / "index.html"
    if index_path.exists():
        return index_path.read_text(encoding="utf-8")
    return "<html><body>Urban Flood API</body></html>"


@app.get("/dashboard", response_class=HTMLResponse)
def read_dashboard():
    index_path = STATIC_DIR / "index.html"
    if index_path.exists():
        return index_path.read_text(encoding="utf-8")
    return HTMLResponse(content="<html><body>Dashboard not found</body></html>", status_code=404)


@app.get("/api/v1/health")
def health_check():
    return {"status": "healthy"}
