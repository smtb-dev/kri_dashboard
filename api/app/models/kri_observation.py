from datetime import date, datetime

from sqlalchemy import Date, DateTime, Float, ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class KRIObservation(Base):
    __tablename__ = "kri_observations"
    __table_args__ = (UniqueConstraint("kri_definition_id", "entry_date", "source_file_id", name="uq_kri_observation"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    kri_definition_id: Mapped[int] = mapped_column(ForeignKey("kri_definitions.id"), nullable=False, index=True)
    source_file_id: Mapped[int] = mapped_column(ForeignKey("source_files.id"), nullable=False, index=True)
    entry_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    current_value: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    kri_definition = relationship("KRIDefinition", back_populates="observations")
    source_file = relationship("SourceFile", back_populates="observations")
    breaches = relationship("KRIBreach", back_populates="observation")
