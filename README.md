# Data Engineering Lab

Practical, reproducible data engineering exercises: ingest → clean → load → query.

## What this repo is
A small collection of pipeline projects built in Python + SQL with clear run steps and repeatable outputs.

## What you'll find
- `pipelines/` ingestion + cleaning scripts
- `sql/` analytics and validation queries
- `data/` local databases + downloaded datasets
- `reports/` generated outputs (CSV summaries)

## Pipelines

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


