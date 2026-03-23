from datetime import date, timedelta

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import and_, desc, func, select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.kri_breach import KRIBreach
from app.models.kri_definition import KRIDefinition
from app.models.kri_observation import KRIObservation
from app.models.kri_threshold import KRIThreshold
from app.schemas.api import BreachOut, KRIDefinitionOut, ObservationOut, ThresholdOut

router = APIRouter(tags=["kri"])


@router.get("/kri", response_model=list[KRIDefinitionOut])
def list_kri(db: Session = Depends(get_db), _=Depends(get_current_user)) -> list[KRIDefinitionOut]:
    rows = db.execute(select(KRIDefinition).order_by(KRIDefinition.category.asc(), KRIDefinition.sub_category.asc())).scalars().all()
    return [KRIDefinitionOut.model_validate(row, from_attributes=True) for row in rows]


@router.get("/kri/{kri_id}")
def get_kri(kri_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)) -> dict:
    kri = db.get(KRIDefinition, kri_id)
    if not kri:
        raise HTTPException(status_code=404, detail="KRI not found")
    thresholds = db.execute(
        select(KRIThreshold).where(KRIThreshold.kri_definition_id == kri_id).order_by(desc(KRIThreshold.version)).limit(1)
    ).scalar_one_or_none()
    breaches = db.execute(
        select(KRIBreach, KRIObservation)
        .join(KRIObservation, KRIBreach.observation_id == KRIObservation.id)
        .where(KRIObservation.kri_definition_id == kri_id)
        .order_by(KRIObservation.entry_date.desc())
        .limit(100)
    ).all()
    return {
        "kri": KRIDefinitionOut.model_validate(kri, from_attributes=True),
        "threshold": ThresholdOut.model_validate(thresholds, from_attributes=True) if thresholds else None,
        "breaches": [
            BreachOut(
                id=b.id,
                severity=b.severity,
                threshold_version=b.threshold_version,
                entry_date=o.entry_date,
                current_value=o.current_value,
            )
            for b, o in breaches
        ],
    }


@router.get("/observations", response_model=list[ObservationOut])
def list_observations(
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
    kri_id: int | None = None,
    category: str | None = None,
    severity: str | None = Query(default=None, pattern="^(RED|AMBER|GREEN)$"),
    start_date: date | None = None,
    end_date: date | None = None,
    q: str | None = None,
) -> list[ObservationOut]:
    query = select(KRIObservation).join(KRIDefinition, KRIObservation.kri_definition_id == KRIDefinition.id)
    if severity:
        query = query.join(KRIBreach, KRIBreach.observation_id == KRIObservation.id).where(KRIBreach.severity == severity)
    filters = []
    if kri_id:
        filters.append(KRIObservation.kri_definition_id == kri_id)
    if category:
        filters.append(KRIDefinition.category == category)
    if start_date:
        filters.append(KRIObservation.entry_date >= start_date)
    if end_date:
        filters.append(KRIObservation.entry_date <= end_date)
    if q:
        like = f"%{q}%"
        filters.append(KRIDefinition.sub_category.ilike(like))
    if filters:
        query = query.where(and_(*filters))
    rows = db.execute(query.order_by(KRIObservation.entry_date.desc()).limit(2000)).scalars().all()
    return [ObservationOut.model_validate(r, from_attributes=True) for r in rows]


@router.get("/kri/{kri_id}/observations", response_model=list[ObservationOut])
def list_kri_observations(kri_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)) -> list[ObservationOut]:
    rows = db.execute(
        select(KRIObservation)
        .where(KRIObservation.kri_definition_id == kri_id)
        .order_by(KRIObservation.entry_date.asc())
    ).scalars().all()
    return [ObservationOut.model_validate(r, from_attributes=True) for r in rows]


@router.get("/dashboard/reds-per-month")
def reds_per_month(db: Session = Depends(get_db), _=Depends(get_current_user)) -> list[dict]:
    month_bucket = func.date_trunc("month", KRIObservation.entry_date)
    rows = db.execute(
        select(month_bucket.label("month_bucket"), func.count(KRIBreach.id))
        .join(KRIBreach, KRIBreach.observation_id == KRIObservation.id)
        .where(KRIBreach.severity == "RED")
        .group_by(month_bucket)
        .order_by(month_bucket)
    ).all()
    return [{"month": month.strftime("%Y-%m"), "reds": count} for month, count in rows]


@router.get("/dashboard/top-reds")
def top_reds(db: Session = Depends(get_db), _=Depends(get_current_user)) -> list[dict]:
    start_date = date.today() - timedelta(days=90)
    rows = db.execute(
        select(KRIDefinition.category, KRIDefinition.sub_category, func.count(KRIBreach.id).label("red_count"))
        .join(KRIObservation, KRIObservation.kri_definition_id == KRIDefinition.id)
        .join(KRIBreach, KRIBreach.observation_id == KRIObservation.id)
        .where(KRIBreach.severity == "RED", KRIObservation.entry_date >= start_date)
        .group_by(KRIDefinition.category, KRIDefinition.sub_category)
        .order_by(desc("red_count"))
        .limit(10)
    ).all()
    return [{"category": c, "sub_category": s, "red_count": rc} for c, s, rc in rows]
