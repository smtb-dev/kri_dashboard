import csv
import hashlib
import io
from datetime import datetime

from fastapi import HTTPException, UploadFile, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.kri_definition import KRIDefinition
from app.models.kri_observation import KRIObservation
from app.models.source_file import SourceFile
from app.models.user import User
from app.services.breaches import recompute_breaches
from app.services.thresholds import recompute_thresholds

REQUIRED_COLUMNS = {"entrydate", "category", "subcategory", "currentvalue"}


def _normalize_header(value: str) -> str:
    return value.strip().lower()


def ingest_csv_upload(db: Session, file: UploadFile, uploaded_by: User) -> SourceFile:
    raw = file.file.read()
    sha = hashlib.sha256(raw).hexdigest()
    existing = db.execute(select(SourceFile).where(SourceFile.sha256 == sha)).scalar_one_or_none()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This file has already been uploaded. Please upload a new file.",
        )

    text = raw.decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(text))
    if not reader.fieldnames:
        raise HTTPException(status_code=400, detail="CSV has no header row")

    normalized_map = {_normalize_header(name): name for name in reader.fieldnames}
    if not REQUIRED_COLUMNS.issubset(set(normalized_map.keys())):
        missing = REQUIRED_COLUMNS - set(normalized_map.keys())
        raise HTTPException(status_code=400, detail=f"Missing required columns: {', '.join(sorted(missing))}")

    source = SourceFile(
        filename=file.filename or "upload.csv",
        sha256=sha,
        row_count=0,
        uploaded_by_id=uploaded_by.id,
        uploaded_at=datetime.utcnow(),
        errors=None,
    )
    db.add(source)
    db.flush()

    row_count = 0
    errors: list[str] = []
    for idx, row in enumerate(reader, start=2):
        try:
            category = row[normalized_map["category"]].strip()
            sub_category = row[normalized_map["subcategory"]].strip()
            date_val = datetime.strptime(row[normalized_map["entrydate"]].strip(), "%m/%d/%Y").date()
            current_value = float(row[normalized_map["currentvalue"]].strip())
            kri = db.execute(
                select(KRIDefinition).where(
                    KRIDefinition.category == category,
                    KRIDefinition.sub_category == sub_category,
                )
            ).scalar_one_or_none()
            if not kri:
                kri = KRIDefinition(category=category, sub_category=sub_category)
                db.add(kri)
                db.flush()

            db.add(
                KRIObservation(
                    kri_definition_id=kri.id,
                    source_file_id=source.id,
                    entry_date=date_val,
                    current_value=current_value,
                )
            )
            row_count += 1
        except Exception as exc:  # noqa: BLE001
            errors.append(f"Line {idx}: {exc}")

    source.row_count = row_count
    source.errors = "\n".join(errors) if errors else None
    db.commit()

    recompute_thresholds(db)
    recompute_breaches(db)
    return source
