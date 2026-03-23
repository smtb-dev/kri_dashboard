from sqlalchemy import delete, func, select
from sqlalchemy.orm import Session

from app.models.kri_breach import KRIBreach
from app.models.kri_observation import KRIObservation
from app.models.kri_threshold import KRIThreshold, ThresholdMethod


def recompute_breaches(db: Session) -> None:
    db.execute(delete(KRIBreach))
    latest_version = db.execute(select(func.max(KRIThreshold.version))).scalar()
    if not latest_version:
        db.commit()
        return
    thresholds = db.execute(select(KRIThreshold).where(KRIThreshold.version == latest_version)).scalars().all()

    for threshold in thresholds:
        observations = db.execute(
            select(KRIObservation).where(KRIObservation.kri_definition_id == threshold.kri_definition_id)
        ).scalars().all()
        for obs in observations:
            severity = "GREEN"
            if threshold.method == ThresholdMethod.percentile.value and threshold.red_value is not None and threshold.amber_value is not None:
                if obs.current_value >= threshold.red_value:
                    severity = "RED"
                elif obs.current_value >= threshold.amber_value:
                    severity = "AMBER"
            breach = KRIBreach(
                observation_id=obs.id,
                threshold_id=threshold.id,
                threshold_version=threshold.version,
                severity=severity,
            )
            db.add(breach)
    db.commit()
