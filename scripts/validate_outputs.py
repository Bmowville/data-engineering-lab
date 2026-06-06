import csv
import sqlite3
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "titanic.db"
REPORT_PATH = ROOT / "reports" / "titanic_summary.csv"
SQL_DIR = ROOT / "sql"

EXPECTED_REPORT_COLUMNS = [
    "sex",
    "passenger_class",
    "total_passengers",
    "avg_age",
    "survival_rate_pct",
]
EXPECTED_GROUPS = {
    ("female", "1"),
    ("female", "2"),
    ("female", "3"),
    ("male", "1"),
    ("male", "2"),
    ("male", "3"),
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def validate_database() -> int:
    require(DB_PATH.exists(), f"Missing database: {DB_PATH}")

    with sqlite3.connect(DB_PATH) as conn:
        table_count = conn.execute(
            "SELECT COUNT(*) FROM sqlite_master WHERE type = 'table' AND name = 'titanic'"
        ).fetchone()[0]
        require(table_count == 1, "Expected titanic table to exist")

        columns = [row[1] for row in conn.execute("PRAGMA table_info(titanic)").fetchall()]
        for column in ["Survived", "Pclass", "Sex", "Age"]:
            require(column in columns, f"Missing required source column: {column}")

        row_count = conn.execute("SELECT COUNT(*) FROM titanic").fetchone()[0]
        require(row_count == 891, f"Expected 891 Titanic rows, found {row_count}")

        for sql_file in sorted(SQL_DIR.glob("*.sql")):
            query = sql_file.read_text(encoding="utf-8")
            rows = conn.execute(query).fetchall()
            require(rows, f"Query returned no rows: {sql_file.name}")

    return row_count


def validate_report(expected_total: int) -> None:
    require(REPORT_PATH.exists(), f"Missing report: {REPORT_PATH}")

    with REPORT_PATH.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        require(reader.fieldnames == EXPECTED_REPORT_COLUMNS, "Unexpected Titanic report columns")
        rows = list(reader)

    require(len(rows) == 6, f"Expected 6 sex/class report rows, found {len(rows)}")

    groups = {(row["sex"], row["passenger_class"]) for row in rows}
    require(groups == EXPECTED_GROUPS, f"Unexpected report groups: {sorted(groups)}")

    total_passengers = sum(int(row["total_passengers"]) for row in rows)
    require(
        total_passengers == expected_total,
        f"Report passenger total {total_passengers} does not match source total {expected_total}",
    )

    for row in rows:
        survival_rate = float(row["survival_rate_pct"])
        require(0.0 <= survival_rate <= 100.0, f"Invalid survival rate: {survival_rate}")


def main() -> None:
    row_count = validate_database()
    validate_report(row_count)
    print("Validated Titanic SQLite table, SQL queries, and summary report")


if __name__ == "__main__":
    main()