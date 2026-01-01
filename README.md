# Data Engineering Lab

Practical, reproducible data engineering exercises: ingest → clean → load → query.

## What this repo is
A small collection of pipeline projects built in Python + SQL with clear run steps and repeatable outputs.

## What you'll find
- `pipelines/` ingestion + cleaning scripts
- `sql/` analytics and validation queries
- `data/` small sample data (or generated)
- `reports/` generated outputs (CSV summaries)

## First pipeline (coming next)
Load a public dataset into a local database (SQLite) and produce summary tables + a simple report.

## Setup
This repo will stay lightweight and runnable locally. Setup instructions will live here as the first pipeline lands.

## How to run
```bash
pip install -r requirements.txt
python pipelines/01_ingest_to_sqlite.py
