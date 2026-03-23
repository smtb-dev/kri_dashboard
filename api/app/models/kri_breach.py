import enum
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class BreachSeverity(str, enum.Enum):
    green = "GREEN"
    amber = "AMBER"
    red = "RED"


class KRIBreach(Base):
    __tablename__ = "kri_breaches"

    id: Mapped[int] = mapped_column(primary_key=True)
    observation_id: Mapped[int] = mapped_column(ForeignKey("kri_observations.id"), nullable=False, index=True)
    threshold_id: Mapped[int] = mapped_column(ForeignKey("kri_thresholds.id"), nullable=False, index=True)
    threshold_version: Mapped[int] = mapped_column(nullable=False)
    severity: Mapped[str] = mapped_column(String(16), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    observation = relationship("KRIObservation", back_populates="breaches")
    threshold = relationship("KRIThreshold", back_populates="breaches")
