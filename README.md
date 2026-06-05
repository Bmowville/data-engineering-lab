# Data Engineering Lab

[![CI](https://github.com/Bmowville/data-engineering-lab/actions/workflows/ci.yml/badge.svg)](https://github.com/Bmowville/data-engineering-lab/actions/workflows/ci.yml)

Practical, reproducible data engineering exercises: ingest → clean → load → query.

## What this repo is
A small collection of pipeline projects built in Python + SQL with clear run steps and repeatable outputs.

Each pipeline starts from an external or raw source, lands data in SQLite, and writes a report that can be inspected without extra services.

## What you'll find
- `pipelines/` ingestion + cleaning scripts
- `sql/` analytics and validation queries
- `scripts/` generated-output validation checks
- `data/` local databases + downloaded datasets
- `reports/` generated outputs (CSV summaries)

## Quick start
Windows PowerShell:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python pipelines/01_ingest_to_sqlite.py
python scripts/validate_outputs.py
```

macOS/Linux:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python pipelines/01_ingest_to_sqlite.py
python scripts/validate_outputs.py
```

After the first run, inspect:
- `data/demo.db`
- `reports/titanic_summary.csv`

## Technical review path
1. Run the Titanic pipeline to verify ingest, load, and reporting from a clean checkout.
2. Run `python scripts/validate_outputs.py` to verify the SQLite table, SQL files, and summary report.
3. Review `docs/pipeline-contracts.md` for the expected inputs, storage targets, and output checks.
4. Review `sql/` for the analytics queries behind the reports.
5. Run the weather pipeline to see an append-style API ingestion example.
6. Compare generated CSV reports with the preview screenshots below.

## Skills demonstrated
- Python pipeline structure with explicit data and report paths
- CSV ingestion, API ingestion, SQLite loading, and SQL-based summaries
- Reproducible local outputs that do not require cloud credentials
- Data contract validation for generated tables, report schemas, and SQL query execution
- CI smoke test for the CSV pipeline

## Pipelines

| Pipeline | Source | Storage | Output | CI |
| --- | --- | --- | --- | --- |
| Titanic CSV | Public CSV download | `data/demo.db` | `reports/titanic_summary.csv` | Yes |
| Weather API | Open-Meteo current weather API | `data/weather.db` | `reports/weather_summary.csv` | Manual, live API |

## Validation
The Titanic pipeline has a local validation script and CI coverage:

```bash
python pipelines/01_ingest_to_sqlite.py
python scripts/validate_outputs.py
```

The validation step checks the generated SQLite table, executes the SQL files in `sql/`, verifies the report schema, and confirms the grouped passenger counts reconcile to the source table.

See `docs/pipeline-contracts.md` for the current pipeline contracts.

### 1) Titanic CSV → SQLite → report
Creates:
- `data/demo.db`
- `reports/titanic_summary.csv`

Run:
```bash
python pipelines/01_ingest_to_sqlite.py
```

### 2) Weather API → SQLite → report
Appends current weather snapshots for a few cities.

Creates:
- `data/weather.db`

Updates:
- `reports/weather_summary.csv`

Run:
```bash
python pipelines/02_weather_api_to_sqlite.py
```

### Titanic summary preview
![Titanic summary preview](https://github.com/user-attachments/assets/b6587f95-f00c-4265-bade-1b67a7b5dabe)

### Weather summary preview
![weather](https://github.com/user-attachments/assets/82c37c8e-ddc8-4886-98b0-ca70ff5f4b77)


