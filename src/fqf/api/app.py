"""FastAPI application factory."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fqf.api.act_routes import router as act_router

API_TITLE = "FQF 2026 Schedule Builder"
CORS_ALLOW_ORIGINS = ["http://localhost:5173", "http://localhost:8000"]


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(title=API_TITLE)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=CORS_ALLOW_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(act_router)

    return app
