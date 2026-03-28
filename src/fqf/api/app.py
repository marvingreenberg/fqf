"""FastAPI application factory."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from fqf.api.act_routes import router as act_router
from fqf.api.schedule_routes import router as schedule_router
from fqf.api.stage_routes import router as stage_router
from fqf.db import close_pool, init_pool

API_TITLE = "FQF 2026 Schedule Builder"
CORS_ALLOW_ORIGINS = ["http://localhost:5173", "http://localhost:8000"]


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Initialize and tear down the database pool."""
    await init_pool()
    yield
    await close_pool()


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(title=API_TITLE, lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=CORS_ALLOW_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(act_router)
    app.include_router(schedule_router)
    app.include_router(stage_router)

    # Static mount must be last — it catches all remaining paths for SPA routing
    static_dir = Path(__file__).parent.parent / "static"
    if static_dir.is_dir():
        app.mount("/", StaticFiles(directory=str(static_dir), html=True), name="static")

    return app
