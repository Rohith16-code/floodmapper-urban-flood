"""Entry point with static frontend mount."""
import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Real-Time Urban Flood Inundation Mapping", version="1.0.0")

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR.parent / "static"

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/")
def read_root():
    return {"message": "Welcome to the Urban Flood Inundation Mapping API"}


@app.get("/dashboard")
def read_dashboard():
    index_path = STATIC_DIR / "index.html"
    if index_path.exists():
        return index_path.read_text()
    return {"error": "Dashboard not found"}