from fastapi import APIRouter

from app.api.routes import auth, dashboard, exports, kri, reports, uploads

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(uploads.router)
api_router.include_router(kri.router)
api_router.include_router(dashboard.router)
api_router.include_router(reports.router)
api_router.include_router(exports.router)
