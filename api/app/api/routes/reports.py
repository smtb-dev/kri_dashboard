from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.schemas.api import ReportRequest
from app.services.reports import build_monthly_pdf

router = APIRouter(prefix="/reports", tags=["reports"])
REPORT_DIR = Path("reports")


@router.post("/pdf")
def generate_pdf(payload: ReportRequest, db: Session = Depends(get_db), _=Depends(get_current_user)) -> dict:
    report_id = f"{payload.month}_{uuid4().hex[:8]}"
    report_path = REPORT_DIR / f"{report_id}.pdf"
    build_monthly_pdf(db, payload.month, report_path)
    return {"id": report_id, "filename": report_path.name}


@router.get("/{report_id}/download")
def download_report(report_id: str, _=Depends(get_current_user)) -> FileResponse:
    path = REPORT_DIR / f"{report_id}.pdf"
    if not path.exists():
        raise HTTPException(status_code=404, detail="Report not found")
    return FileResponse(path, media_type="application/pdf", filename=path.name)
