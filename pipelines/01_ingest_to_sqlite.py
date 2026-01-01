import sqlite3
from pathlib import Path

import pandas as pd
import requests

DATA_DIR = Path("data")
REPORTS_DIR = Path("reports")

CSV_URL = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
CSV_PATH = DATA_DIR / "titanic.csv"
DB_PATH = DATA_DIR / "demo.db"
REPORT_PATH = REPORTS_DIR / "titanic_summary.csv"


def download_csv(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        return

    r = requests.get(url, timeout=30)
    r.raise_for_status()
    dest.write_bytes(r.content)


def load_to_sqlite(csv_path: Path, db_path: Path) -> None:
    df = pd.read_csv(csv_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(db_path) as conn:
        df.to_sql("titanic", conn, if_exists="replace", index=False)


def write_report(db_path: Path, report_path: Path) -> None:
    query = """
    SELECT
        Sex AS sex,
        Pclass AS passenger_class,
        COUNT(*) AS total_passengers,
        ROUND(AVG(Age), 2) AS avg_age,
        ROUND(AVG(Survived) * 100.0, 2) AS survival_rate_pct
    FROM titanic
    GROUP BY Sex, Pclass
    ORDER BY Sex, Pclass;
    """

    with sqlite3.connect(db_path) as conn:
        out = pd.read_sql_query(query, conn)

    report_path.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(report_path, index=False)


def main() -> None:
    download_csv(CSV_URL, CSV_PATH)
    load_to_sqlite(CSV_PATH, DB_PATH)
    write_report(DB_PATH, REPORT_PATH)
    print(f"Created: {DB_PATH}")
    print(f"Created: {REPORT_PATH}")


if __name__ == "__main__":
    main()
