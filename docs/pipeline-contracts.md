# Pipeline Contracts

This repo keeps each pipeline contract small enough to run locally and specific enough to validate in CI.

## Current Pipelines

| Pipeline | Input | Storage | Report | Validation |
| --- | --- | --- | --- | --- |
| Titanic CSV | Public CSV downloaded to `data/titanic.csv` | SQLite table `titanic` in `data/titanic.db` | `reports/titanic_summary.csv`, `reports/data_quality_report.md` | Automated in CI |
| Weather API | Open-Meteo current weather response | SQLite table `weather_current` in `data/weather.db` | `reports/weather_summary.csv` | Manual because it depends on a live API |

## Titanic Contract

The Titanic pipeline is the CI-backed reference pipeline.

Expected source fields:
- `Survived`
- `Pclass`
- `Sex`
- `Age`

Expected SQLite output:
- Database path: `data/titanic.db`
- Table: `titanic`
- Row count: 891

Expected report output:
- Path: `reports/titanic_summary.csv`
- Columns: `sex`, `passenger_class`, `total_passengers`, `avg_age`, `survival_rate_pct`
- Groups: female/male by passenger classes 1, 2, and 3
- Passenger totals reconcile to the `titanic` source table
- Survival rates stay within 0 to 100 percent

Expected quality report output:
- Path: `reports/data_quality_report.md`
- Sections: Summary, Missing Values, Numeric Ranges
- Row count: 891
- Duplicate `PassengerId` values: 0
- Missing expected columns: none

Run locally:

```bash
python pipelines/01_ingest_to_sqlite.py
python scripts/generate_data_quality_report.py
python scripts/validate_outputs.py
```

## SQL Query Checks

`scripts/validate_outputs.py` executes every `.sql` file in `sql/` against `data/titanic.db`. This keeps the example analytics queries connected to the generated table instead of becoming stale documentation.

## Weather Contract

The weather pipeline is intentionally kept out of CI because it depends on a live third-party API. It is still useful as an example of append-style ingestion.

Expected SQLite output:
- Database path: `data/weather.db`
- Table: `weather_current`

Expected report output:
- Path: `reports/weather_summary.csv`
- One row per configured city
- Observation counts increase as the pipeline is run over time