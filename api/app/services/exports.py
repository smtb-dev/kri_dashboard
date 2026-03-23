from datetime import date
from io import BytesIO

from openpyxl import Workbook
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.kri_definition import KRIDefinition
from app.models.kri_observation import KRIObservation


def export_excel(db: Session, date_start: str | None, date_end: str | None, category: str | None) -> bytes:
    parsed_start = date.fromisoformat(date_start) if date_start else None
    parsed_end = date.fromisoformat(date_end) if date_end else None
    workbook = Workbook()
    ws = workbook.active
    ws.title = "KRI Export"
    ws.append(["EntryDate", "Category", "SubCategory", "CurrentValue"])

    query = (
        select(KRIObservation, KRIDefinition)
        .join(KRIDefinition, KRIObservation.kri_definition_id == KRIDefinition.id)
        .order_by(KRIObservation.entry_date.asc())
    )
    if parsed_start:
        query = query.where(KRIObservation.entry_date >= parsed_start)
    if parsed_end:
        query = query.where(KRIObservation.entry_date <= parsed_end)
    if category:
        query = query.where(KRIDefinition.category == category)

    for obs, kri in db.execute(query).all():
        ws.append([obs.entry_date.isoformat(), kri.category, kri.sub_category, obs.current_value])

    data = BytesIO()
    workbook.save(data)
    return data.getvalue()
