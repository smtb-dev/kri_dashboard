from datetime import datetime

from sqlalchemy import DateTime, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class KRIDefinition(Base):
    __tablename__ = "kri_definitions"
    __table_args__ = (UniqueConstraint("category", "sub_category", name="uq_kri_category_subcategory"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    category: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    sub_category: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    observations = relationship("KRIObservation", back_populates="kri_definition")
    thresholds = relationship("KRIThreshold", back_populates="kri_definition")
