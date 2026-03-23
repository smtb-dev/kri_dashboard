from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.schemas.api import DashboardSummaryOut
from app.services.dashboard import get_summary

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary", response_model=DashboardSummaryOut)
def dashboard_summary(db: Session = Depends(get_db), _=Depends(get_current_user)) -> DashboardSummaryOut:
    return DashboardSummaryOut(**get_summary(db))
