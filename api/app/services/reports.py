from pathlib import Path

from jinja2 import Template
from playwright.sync_api import sync_playwright
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.kri_breach import KRIBreach
from app.models.kri_definition import KRIDefinition
from app.models.kri_observation import KRIObservation


def build_monthly_pdf(db: Session, month: str, output_path: Path) -> Path:
    month_prefix = f"{month}-"
    red_count = db.execute(
        select(func.count(KRIBreach.id))
        .join(KRIObservation, KRIBreach.observation_id == KRIObservation.id)
        .where(KRIBreach.severity == "RED", func.to_char(KRIObservation.entry_date, "YYYY-MM-DD").like(f"{month_prefix}%"))
    ).scalar_one()

    top_rows = db.execute(
        select(KRIDefinition.sub_category, func.count(KRIBreach.id).label("count"))
        .join(KRIObservation, KRIBreach.observation_id == KRIObservation.id)
        .join(KRIDefinition, KRIObservation.kri_definition_id == KRIDefinition.id)
        .where(KRIBreach.severity == "RED", func.to_char(KRIObservation.entry_date, "YYYY-MM-DD").like(f"{month_prefix}%"))
        .group_by(KRIDefinition.sub_category)
        .order_by(func.count(KRIBreach.id).desc())
        .limit(10)
    ).all()

    template = Template(
        """
        <html><head><style>
        body { font-family: Arial; padding: 32px; }
        h1, h2 { margin-bottom: 8px; }
        table { border-collapse: collapse; width: 100%; margin-top: 8px; }
        td, th { border: 1px solid #ddd; padding: 8px; text-align: left; }
        </style></head><body>
        <h1>KRI Monthly Report - {{ month }}</h1>
        <p>Executive summary: total red breaches {{ red_count }}.</p>
        <h2>Top Red KRIs</h2>
        <table><thead><tr><th>KRI</th><th>Red Count</th></tr></thead><tbody>
        {% for row in top_rows %}
        <tr><td>{{ row[0] }}</td><td>{{ row[1] }}</td></tr>
        {% endfor %}
        </tbody></table>
        </body></html>
        """
    )
    html = template.render(month=month, red_count=red_count, top_rows=top_rows)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_content(html)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        page.pdf(path=str(output_path), format="A4")
        browser.close()

    return output_path
