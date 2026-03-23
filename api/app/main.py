from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import get_settings
from app.db.session import SessionLocal
from app.services.seed_demo_data import seed_demo_data, seed_initial_admin

settings = get_settings()
app = FastAPI(title=settings.app_name)
app.include_router(api_router, prefix=settings.api_prefix)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[x.strip() for x in settings.cors_origins.split(",")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.on_event("startup")
def startup_seed() -> None:
    if not settings.seed_enabled:
        return
    try:
        db = SessionLocal()
        try:
            seed_initial_admin(db)
            seed_demo_data(db)
        finally:
            db.close()
    except Exception:
        # In test/local bootstrap contexts where DB is not ready yet, app still starts.
        return
