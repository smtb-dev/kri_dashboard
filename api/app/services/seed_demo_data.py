import hashlib
import random
from datetime import UTC, date, datetime, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.security import hash_password
from app.models.kri_definition import KRIDefinition
from app.models.kri_observation import KRIObservation
from app.models.source_file import SourceFile
from app.models.user import User, UserRole
from app.services.breaches import recompute_breaches
from app.services.thresholds import recompute_thresholds

CATALOG: dict[str, list[str]] = {
    "Security Event Continuous Monitoring": [
        "DDOS",
        "Privilege Escalations",
        "WAF Blocks",
        "Ransomware Signals",
        "Auth Bypass Attempts",
        "Firewall Rule Changes",
        "Suspicious Lateral Movement",
    ],
    "Data Breach": [
        "High Impact Leak Indicators",
        "Medium Impact Leak Indicators",
        "Low Impact Leak Indicators",
        "Public Bucket Exposures",
        "Sensitive Records Accessed",
    ],
    "Endpoint Protection Alerts": [
        "Malware Detections",
        "Suspicious Activity Alerts",
        "EDR Quarantines",
        "Unapproved Software Executions",
        "Credential Dumping Signals",
    ],
    "Identity and Access": [
        "MFA Failures",
        "Dormant Privileged Accounts",
        "New Admin Accounts",
        "Impossible Travel Logins",
        "Password Reset Spikes",
    ],
    "Vulnerability Management": [
        "Critical Vulns Discovered",
        "SLA Breach Count",
        "Internet Exposure Count",
        "Unpatched High Vulns",
        "Remediation Backlog",
        "Aging Critical Findings",
    ],
    "Email Security and Phishing Campaigns": [
        "Quarterly Campaign Failure Rate",
        "Quarterly Click Through",
        "Quarterly Credential Submission",
        "Quarterly Repeat Offenders",
        "Quarterly Reporting Delay",
    ],
    "DLP and Data Handling": [
        "DLP Policy Violations",
        "Data Whitelisting Requests",
        "Unencrypted Transfer Attempts",
        "Restricted Data Share Events",
        "USB Data Copy Alerts",
    ],
    "Cloud Security Posture": [
        "Misconfigured IAM Policies",
        "Public Service Endpoints",
        "Failed Compliance Checks",
        "Unapproved Key Creation",
        "Container Escape Signals",
    ],
    "Third Party Risk": [
        "Critical Vendor Findings",
        "Expired Security Attestations",
        "Open Vendor Exceptions",
        "Vendor Breach Notifications",
        "Delayed Remediation Plans",
    ],
}


def _campaign_series(day_index: int, rng: random.Random) -> float:
    if day_index % 90 != 0:
        return -1.0
    return max(0.0, round(rng.normalvariate(6.0, 2.0), 2))


def _daily_series(base: float, season_factor: float, rng: random.Random, in_incident: bool) -> float:
    value = max(0.0, rng.poisson(base) if hasattr(rng, "poisson") else rng.normalvariate(base, 1.5))
    value *= season_factor
    if in_incident:
        value += rng.uniform(8.0, 20.0)
    if rng.random() < 0.03:
        value += rng.uniform(12.0, 30.0)
    return round(max(0.0, value), 2)


def _season(month: int) -> float:
    if month in (11, 12):
        return 1.4
    if month in (6, 7, 8):
        return 1.2
    return 1.0


def _incident_windows() -> list[tuple[date, date]]:
    return [(date(2025, 3, 2), date(2025, 3, 14)), (date(2025, 10, 5), date(2025, 10, 20))]


def _is_campaign(sub_category: str) -> bool:
    return "Quarterly" in sub_category


def _is_in_incident_window(entry_date: date) -> bool:
    for start, end in _incident_windows():
        if start <= entry_date <= end:
            return True
    return False


def seed_initial_admin(db: Session) -> None:
    settings = get_settings()
    existing = db.execute(select(User).where(User.username == settings.admin_username)).scalar_one_or_none()
    if existing:
        return
    db.add(User(username=settings.admin_username, password_hash=hash_password(settings.admin_password), role=UserRole.admin))
    db.commit()


def seed_demo_data(db: Session) -> None:
    settings = get_settings()
    has_data = db.execute(select(KRIObservation.id).limit(1)).first()
    if has_data:
        return

    rng = random.Random(20250224)
    definitions: dict[tuple[str, str], KRIDefinition] = {}
    for category, subcategories in CATALOG.items():
        for sub in subcategories:
            row = KRIDefinition(category=category.strip(), sub_category=sub.strip())
            db.add(row)
            db.flush()
            definitions[(category, sub)] = row

    admin = db.execute(select(User).where(User.username == settings.admin_username)).scalar_one_or_none()
    uploaded_at = datetime.now(UTC) - timedelta(days=3 if settings.demo_stale else 0)
    seed_sha = hashlib.sha256(b"seed-2025-baseline").hexdigest()
    seed_source = SourceFile(
        filename="seed_2025_baseline.csv",
        sha256=seed_sha,
        row_count=0,
        uploaded_by_id=admin.id if admin else None,
        uploaded_at=uploaded_at,
        errors=None,
    )
    db.add(seed_source)
    db.flush()

    start = date(2025, 1, 1)
    end = date(2025, 12, 31)
    total_rows = 0
    current = start
    while current <= end:
        for (category, sub), kri in definitions.items():
            if _is_campaign(sub):
                value = _campaign_series((current - start).days, rng)
                if value < 0:
                    continue
            else:
                base = 1.0 + (len(sub) % 4)
                value = _daily_series(base, _season(current.month), rng, _is_in_incident_window(current))
            db.add(
                KRIObservation(
                    kri_definition_id=kri.id,
                    source_file_id=seed_source.id,
                    entry_date=current,
                    current_value=value,
                )
            )
            total_rows += 1
        current += timedelta(days=1)

    seed_source.row_count = total_rows
    db.commit()
    recompute_thresholds(db)
    recompute_breaches(db)
