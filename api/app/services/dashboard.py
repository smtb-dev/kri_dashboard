from datetime import UTC, date, datetime

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.kri_breach import KRIBreach
from app.models.kri_definition import KRIDefinition
from app.models.kri_observation import KRIObservation
from app.models.source_file import SourceFile


def _days_since(ts: datetime | None) -> int | None:
    if not ts:
        return None
    return (datetime.now(UTC) - ts.replace(tzinfo=UTC)).days


def get_summary(db: Session) -> dict:
    today = date.today()
    month_start = today.replace(day=1)
    year_start = today.replace(month=1, day=1)

    last_upload = db.execute(select(func.max(SourceFile.uploaded_at))).scalar_one_or_none()
    days = _days_since(last_upload)
    stale = days is None or days > 2

    reds_mtd = db.execute(
        select(func.count(KRIBreach.id))
        .join(KRIObservation, KRIBreach.observation_id == KRIObservation.id)
        .where(KRIBreach.severity == "RED", KRIObservation.entry_date >= month_start)
    ).scalar_one()
    reds_ytd = db.execute(
        select(func.count(KRIBreach.id))
        .join(KRIObservation, KRIBreach.observation_id == KRIObservation.id)
        .where(KRIBreach.severity == "RED", KRIObservation.entry_date >= year_start)
    ).scalar_one()
    ambers_mtd = db.execute(
        select(func.count(KRIBreach.id))
        .join(KRIObservation, KRIBreach.observation_id == KRIObservation.id)
        .where(KRIBreach.severity == "AMBER", KRIObservation.entry_date >= month_start)
    ).scalar_one()
    ambers_ytd = db.execute(
        select(func.count(KRIBreach.id))
        .join(KRIObservation, KRIBreach.observation_id == KRIObservation.id)
        .where(KRIBreach.severity == "AMBER", KRIObservation.entry_date >= year_start)
    ).scalar_one()
    total_kris = db.execute(select(func.count(KRIDefinition.id))).scalar_one()

    return {
        "reds_mtd": reds_mtd,
        "reds_ytd": reds_ytd,
        "ambers_mtd": ambers_mtd,
        "ambers_ytd": ambers_ytd,
        "total_kris": total_kris,
        "last_upload_at": last_upload,
        "stale": stale,
        "days_since_upload": days,
    }
