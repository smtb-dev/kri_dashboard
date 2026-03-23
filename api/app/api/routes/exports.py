from fastapi import APIRouter, Depends, Query
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.services.exports import export_excel

router = APIRouter(prefix="/exports", tags=["exports"])


@router.get("/excel")
def download_excel(
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
    start_date: str | None = Query(default=None),
    end_date: str | None = Query(default=None),
    category: str | None = Query(default=None),
) -> Response:
    content = export_excel(db, start_date, end_date, category)
    return Response(
        content=content,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": 'attachment; filename="kri_export.xlsx"'},
    )
