"""Application entry point for real-time-urban-flood-inundation-mapping."""
import os
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from src.config.settings import ENV, DEBUG, ML_MODEL_PATH, API_HOST, API_PORT
from src.utils.logger import get_logger

logger = get_logger("real-time-urban-flood-inundation-mapping.main")
STATIC_DIR = Path(__file__).parent.parent / "static"


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup/shutdown lifecycle — degrade gracefully if model missing."""
    logger.info(f"Starting real-time-urban-flood-inundation-mapping in {ENV} mode")
    try:
        from src.db.cache import CacheClient
        app.state.cache = CacheClient()
    except Exception as e:
        logger.warning(f"Cache unavailable: {e}")
    try:
        from src.ml.model_loader import ModelLoader
        app.state.model = ModelLoader().load(ML_MODEL_PATH)
        logger.info(f"Model loaded from {ML_MODEL_PATH}")
    except Exception as e:
        logger.warning(f"Model load failed: {e}; running degraded")
        app.state.model = None
    yield
    logger.info("Shutdown complete")


def create_app() -> FastAPI:
    """Factory function — creates and configures the FastAPI app."""
    app = FastAPI(
        title="real-time-urban-flood-inundation-mapping",
        description="Urban flooding displaces millions annually, and city emergency managers lack real-time, street-level",
        version="1.0.0",
        debug=DEBUG,
        lifespan=lifespan,
    )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Static frontend
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

    @app.get("/dashboard", tags=["frontend"])
    async def dashboard():
        """Serve the production dashboard."""
        return FileResponse(str(STATIC_DIR / "index.html"))

    # Health check endpoints
    @app.get("/health", tags=["health"])
    async def health():
        return {"status": "healthy", "env": ENV}

    @app.get("/ready", tags=["health"])
    async def ready():
        return {"status": "ready", "model_loaded": getattr(app.state, "model", None) is not None}

    return app


# Global app instance for imports
app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host=API_HOST, port=API_PORT)
