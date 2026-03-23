from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.source_file import SourceFile
from app.models.user import User
from app.schemas.api import UploadOut
from app.services.uploads import ingest_csv_upload

router = APIRouter(prefix="/uploads", tags=["uploads"])


@router.post("", response_model=UploadOut)
def upload_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> UploadOut:
    source = ingest_csv_upload(db, file, user)
    return UploadOut.model_validate(source, from_attributes=True)


@router.get("", response_model=list[UploadOut])
def list_uploads(db: Session = Depends(get_db), _: User = Depends(get_current_user)) -> list[UploadOut]:
    rows = db.execute(select(SourceFile).order_by(SourceFile.uploaded_at.desc())).scalars().all()
    return [UploadOut.model_validate(row, from_attributes=True) for row in rows]
