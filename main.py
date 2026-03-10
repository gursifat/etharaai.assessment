from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import create_tables
from app.routers_employees import router as employees_router
from app.routers_attendance import router as attendance_router


def create_app() -> FastAPI:
    """
    Application factory.

    This keeps FastAPI configuration in one place and makes it
    easier to test or extend later.
    """
    app = FastAPI(title="HRMS Lite")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Health check endpoint stays close to the core app.
    @app.get("/health")
    def health_check():
        return {"status": "ok"}

    # Register routers that contain the actual business endpoints.
    app.include_router(employees_router)
    app.include_router(attendance_router)

    @app.on_event("startup")
    def on_startup():
        create_tables()

    return app


# FastAPI looks for this `app` variable when you run `uvicorn main:app`.
app = create_app()

