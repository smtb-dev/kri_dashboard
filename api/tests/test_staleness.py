from datetime import UTC, datetime, timedelta

from app.models.source_file import SourceFile


def test_dashboard_summary_stale_true_when_older_than_two_days(client) -> None:
    from .conftest import TestingSessionLocal

    db = TestingSessionLocal()
    db.add(
        SourceFile(
            filename="seed.csv",
            sha256="a" * 64,
            row_count=1,
            uploaded_by_id=1,
            uploaded_at=datetime.now(UTC) - timedelta(days=3),
            errors=None,
        )
    )
    db.commit()
    db.close()

    response = client.get("/api/dashboard/summary")
    assert response.status_code == 200
    assert response.json()["stale"] is True
