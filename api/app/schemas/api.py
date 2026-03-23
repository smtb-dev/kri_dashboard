from datetime import date, datetime

from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    role: str


class UploadOut(BaseModel):
    id: int
    filename: str
    sha256: str
    row_count: int
    uploaded_at: datetime
    errors: str | None


class KRIDefinitionOut(BaseModel):
    id: int
    category: str
    sub_category: str


class ObservationOut(BaseModel):
    id: int
    kri_definition_id: int
    entry_date: date
    current_value: float


class ThresholdOut(BaseModel):
    method: str
    amber_percentile: float
    red_percentile: float
    amber_value: float | None
    red_value: float | None
    baseline_start: date
    baseline_end: date
    version: int
    computed_at: datetime


class BreachOut(BaseModel):
    id: int
    severity: str
    threshold_version: int
    entry_date: date
    current_value: float


class DashboardSummaryOut(BaseModel):
    reds_mtd: int
    reds_ytd: int
    ambers_mtd: int
    ambers_ytd: int
    total_kris: int
    last_upload_at: datetime | None
    stale: bool
    days_since_upload: int | None


class ReportRequest(BaseModel):
    month: str = Field(pattern=r"^\d{4}-\d{2}$")
