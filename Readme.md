# KRI Dashboard Demo

Internal demo-ready Key Risk Indicators dashboard for security leadership review.

## Stack
- `web`: Next.js App Router + TypeScript + Tailwind + Recharts + TanStack Table
- `api`: FastAPI + Pydantic + SQLAlchemy 2 + Alembic
- `db`: Postgres
- Auth: bcrypt + JWT in `httpOnly` cookie (`admin`/`viewer`)
- Reporting: Playwright PDF + openpyxl Excel
- Deployment: Docker Compose

## Repository layout
- `api/` FastAPI backend, migrations, seeding, tests
- `web/` Next.js frontend
- `infra/` compose and environment templates

## Quick start (Docker)
1. Copy env template:
   - `cd infra`
   - `cp .env.example .env`
2. Build and run:
   - `docker compose up --build`
3. Open:
   - Web: `http://localhost:3000`
   - API docs: `http://localhost:8000/docs`

Default login (from env):
- username: `admin`
- password: `admin123`

## Demo stale/fresh toggle
Set in `infra/.env`:
- `DEMO_STALE=true` -> seed upload appears as `now-3 days`
- `DEMO_STALE=false` -> seed upload appears as current timestamp

Then recreate:
- `docker compose down -v`
- `docker compose up --build`

## Seed behavior
On first run the API startup flow:
1. Creates initial admin user from env
2. Seeds KRI dictionary (9 categories, 48 subcategories)
3. Seeds 2025 baseline observations (daily + quarterly campaign KRIs)
4. Computes thresholds (p75 amber, p90 red, frozen to 2025)
5. Derives breaches and links to threshold versions
6. Creates seed `source_files` row with demo stale/fresh timestamp

## API endpoints
- `POST /api/auth/login`
- `POST /api/auth/logout`
- `GET /api/auth/me`
- `POST /api/uploads`
- `GET /api/uploads`
- `GET /api/kri`
- `GET /api/kri/{id}`
- `GET /api/observations`
- `GET /api/kri/{id}/observations`
- `GET /api/dashboard/summary`
- `POST /api/reports/pdf`
- `GET /api/reports/{id}/download`
- `GET /api/exports/excel`

## Local backend test run
From `api/`:
- `python3 -m venv .venv`
- `source .venv/bin/activate`
- `pip install -r requirements.txt`
- `pytest -q`

Included tests:
- CSV ingestion schema validation
- Threshold percentile computation
- Staleness summary behavior (`>2 days` => `stale=true`)
kri_dashboard
