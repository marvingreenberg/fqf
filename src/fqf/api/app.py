"""FastAPI application factory."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
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

    static_dir = Path(__file__).parent.parent / "static"
    if static_dir.is_dir():
        # Serve static assets (JS, CSS, images) at their real paths
        app.mount("/_app", StaticFiles(directory=str(static_dir / "_app")), name="static-app")

        # SPA fallback: any non-API path serves index.html for client-side routing
        fallback = static_dir / "index.html"

        @app.get("/{path:path}", include_in_schema=False)
        async def spa_fallback(path: str) -> FileResponse:
            # Serve the actual file if it exists (e.g., favicon.png, fqf-map.png)
            candidate = static_dir / path
            if candidate.is_file():
                return FileResponse(candidate)
            return FileResponse(fallback)

    return app
