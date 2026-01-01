import sqlite3
from pathlib import Path
from datetime import datetime, timezone

import pandas as pd
import requests

DATA_DIR = Path("data")
REPORTS_DIR = Path("reports")

DB_PATH = DATA_DIR / "weather.db"
REPORT_PATH = REPORTS_DIR / "weather_summary.csv"


CITIES = [
    {"city": "New York", "lat": 40.7128, "lon": -74.0060},
    {"city": "Chicago", "lat": 41.8781, "lon": -87.6298},
    {"city": "Dallas", "lat": 32.7767, "lon": -96.7970},
    {"city": "Seattle", "lat": 47.6062, "lon": -122.3321},
]


def fetch_current_weather(lat: float, lon: float) -> dict:
    # Open-Meteo: no API key needed
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": "true",
        "temperature_unit": "fahrenheit",
        "windspeed_unit": "mph",
    }
    r = requests.get(url, params=params, timeout=30)
    r.raise_for_status()
    return r.json()


def build_rows() -> pd.DataFrame:
    rows = []
    for c in CITIES:
        payload = fetch_current_weather(c["lat"], c["lon"])
        cw = payload.get("current_weather", {})
        rows.append(
            {
                "captured_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "city": c["city"],
                "latitude": c["lat"],
                "longitude": c["lon"],
                "temperature_f": cw.get("temperature"),
                "windspeed_mph": cw.get("windspeed"),
                "winddirection_deg": cw.get("winddirection"),
                "weathercode": cw.get("weathercode"),
            }
        )
    return pd.DataFrame(rows)


def write_to_sqlite(df: pd.DataFrame, db_path: Path) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        df.to_sql("weather_current", conn, if_exists="append", index=False)


def write_report(db_path: Path, report_path: Path) -> None:
    query = """
    SELECT
      city,
      COUNT(*) AS observations,
      ROUND(AVG(temperature_f), 2) AS avg_temp_f,
      ROUND(AVG(windspeed_mph), 2) AS avg_windspeed_mph,
      MIN(captured_at_utc) AS first_seen_utc,
      MAX(captured_at_utc) AS last_seen_utc
    FROM weather_current
    GROUP BY city
    ORDER BY city;
    """
    with sqlite3.connect(db_path) as conn:
        out = pd.read_sql_query(query, conn)

    report_path.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(report_path, index=False)


def main() -> None:
    df = build_rows()
    write_to_sqlite(df, DB_PATH)
    write_report(DB_PATH, REPORT_PATH)
    print(f"Appended rows to: {DB_PATH}")
    print(f"Updated report: {REPORT_PATH}")


if __name__ == "__main__":
    main()
