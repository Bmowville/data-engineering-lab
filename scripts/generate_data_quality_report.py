import sqlite3
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "titanic.db"
REPORT_PATH = ROOT / "reports" / "data_quality_report.md"

EXPECTED_COLUMNS = [
    "PassengerId",
    "Survived",
    "Pclass",
    "Name",
    "Sex",
    "Age",
    "SibSp",
    "Parch",
    "Ticket",
    "Fare",
    "Cabin",
    "Embarked",
]
NUMERIC_COLUMNS = ["PassengerId", "Survived", "Pclass", "Age", "SibSp", "Parch", "Fare"]


def fetch_one(conn: sqlite3.Connection, query: str) -> object:
    return conn.execute(query).fetchone()[0]


def markdown_table(headers: list[str], rows: list[list[object]]) -> list[str]:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    lines.extend("| " + " | ".join(str(value) for value in row) + " |" for row in rows)
    return lines


def generate_report(db_path: Path = DB_PATH, report_path: Path = REPORT_PATH) -> None:
    if not db_path.exists():
        raise FileNotFoundError(f"Missing database: {db_path}")

    with sqlite3.connect(db_path) as conn:
        columns = [row[1] for row in conn.execute("PRAGMA table_info(titanic)").fetchall()]
        row_count = int(fetch_one(conn, "SELECT COUNT(*) FROM titanic"))
        missing_columns = [column for column in EXPECTED_COLUMNS if column not in columns]
        duplicate_passenger_ids = int(
            fetch_one(
                conn,
                """
                SELECT COUNT(*)
                FROM (
                    SELECT PassengerId
                    FROM titanic
                    GROUP BY PassengerId
                    HAVING COUNT(*) > 1
                )
                """,
            )
        )

        missing_rows = []
        for column in EXPECTED_COLUMNS:
            if column in columns:
                missing_count = int(
                    fetch_one(conn, f'SELECT COUNT(*) - COUNT("{column}") FROM titanic')
                )
                missing_pct = round((missing_count / row_count) * 100, 2)
                missing_rows.append([column, missing_count, missing_pct])

        range_rows = []
        for column in NUMERIC_COLUMNS:
            if column in columns:
                minimum, maximum = conn.execute(
                    f'SELECT MIN("{column}"), MAX("{column}") FROM titanic'
                ).fetchone()
                range_rows.append([column, minimum, maximum])

    summary_rows = [
        ["Rows", row_count],
        ["Columns", len(columns)],
        ["Missing expected columns", ", ".join(missing_columns) if missing_columns else "none"],
        ["Duplicate PassengerId values", duplicate_passenger_ids],
    ]

    lines = [
        "# Titanic Data Quality Report",
        "",
        "Generated from `data/titanic.db` after the Titanic CSV pipeline runs.",
        "",
        "## Summary",
        "",
        *markdown_table(["Metric", "Value"], summary_rows),
        "",
        "## Missing Values",
        "",
        *markdown_table(["Column", "Missing Count", "Missing Percent"], missing_rows),
        "",
        "## Numeric Ranges",
        "",
        *markdown_table(["Column", "Minimum", "Maximum"], range_rows),
        "",
    ]

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    generate_report()
    print(f"Created: {REPORT_PATH}")


if __name__ == "__main__":
    main()