from datetime import date

import numpy as np
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.kri_definition import KRIDefinition
from app.models.kri_observation import KRIObservation
from app.models.kri_threshold import KRIThreshold, ThresholdMethod

BASELINE_START = date(2025, 1, 1)
BASELINE_END = date(2025, 12, 31)


def compute_percentiles(values: list[float], amber_percentile: float = 75.0, red_percentile: float = 90.0) -> tuple[float, float]:
    amber = float(np.percentile(values, amber_percentile))
    red = float(np.percentile(values, red_percentile))
    return amber, red


def recompute_thresholds(db: Session, amber_percentile: float = 75.0, red_percentile: float = 90.0) -> None:
    current_max_version = db.execute(select(func.max(KRIThreshold.version))).scalar()
    next_version = (current_max_version or 0) + 1

    definitions = db.execute(select(KRIDefinition)).scalars().all()
    for kri in definitions:
        values = db.execute(
            select(KRIObservation.current_value).where(
                KRIObservation.kri_definition_id == kri.id,
                KRIObservation.entry_date >= BASELINE_START,
                KRIObservation.entry_date <= BASELINE_END,
            )
        ).scalars().all()

        if len(values) < 20:
            threshold = KRIThreshold(
                kri_definition_id=kri.id,
                method=ThresholdMethod.needs_manual.value,
                amber_percentile=amber_percentile,
                red_percentile=red_percentile,
                amber_value=None,
                red_value=None,
                baseline_start=BASELINE_START,
                baseline_end=BASELINE_END,
                version=next_version,
            )
        else:
            amber_value, red_value = compute_percentiles(values, amber_percentile, red_percentile)
            threshold = KRIThreshold(
                kri_definition_id=kri.id,
                method=ThresholdMethod.percentile.value,
                amber_percentile=amber_percentile,
                red_percentile=red_percentile,
                amber_value=amber_value,
                red_value=red_value,
                baseline_start=BASELINE_START,
                baseline_end=BASELINE_END,
                version=next_version,
            )
        db.add(threshold)

    db.commit()
