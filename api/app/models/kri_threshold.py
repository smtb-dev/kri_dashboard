import enum
from datetime import date, datetime

from sqlalchemy import Date, DateTime, Float, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class ThresholdMethod(str, enum.Enum):
    percentile = "percentile"
    needs_manual = "needs_manual"


class KRIThreshold(Base):
    __tablename__ = "kri_thresholds"

    id: Mapped[int] = mapped_column(primary_key=True)
    kri_definition_id: Mapped[int] = mapped_column(ForeignKey("kri_definitions.id"), nullable=False, index=True)
    method: Mapped[str] = mapped_column(String(40), nullable=False, default=ThresholdMethod.percentile.value)
    amber_percentile: Mapped[float] = mapped_column(Float, nullable=False, default=75.0)
    red_percentile: Mapped[float] = mapped_column(Float, nullable=False, default=90.0)
    amber_value: Mapped[float | None] = mapped_column(Float, nullable=True)
    red_value: Mapped[float | None] = mapped_column(Float, nullable=True)
    baseline_start: Mapped[date] = mapped_column(Date, nullable=False)
    baseline_end: Mapped[date] = mapped_column(Date, nullable=False)
    computed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    kri_definition = relationship("KRIDefinition", back_populates="thresholds")
    breaches = relationship("KRIBreach", back_populates="threshold")
