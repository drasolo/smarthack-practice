"""Read readings from CSV or Parquet into the clean shape: meter_id, ts (UTC), kwh.

DuckDB does the reading, so a multi-GB file or a folder of CSVs works the same as the sample.
"""

from __future__ import annotations

from pathlib import Path

import duckdb
import pandas as pd

from common import config

# Column names seen in the wild, lower-cased. Add the challenge's names here on day one.
ALIASES = {
    "meter_id": ["meter_id", "pod_id", "pod", "lclid", "meter", "id"],
    "ts": ["ts", "ts_utc", "timestamp", "datetime", "date_time", "time"],
    "kwh": ["kwh", "kwh/hh (per half hour)", "energy_kwh", "consumption", "value"],
}


def source_sql(path: str | Path) -> str:
    """DuckDB table expression for a file, or for every CSV/Parquet file in a folder."""
    path = Path(path)
    if path.is_dir():
        parquet = list(path.glob("*.parquet"))
        pattern = str(path / ("*.parquet" if parquet else "*.csv")).replace("\\", "/")
    else:
        pattern = str(path).replace("\\", "/")
    if pattern.endswith(".parquet"):
        return f"read_parquet('{pattern}')"
    return f"read_csv('{pattern}', all_varchar = true)"


def find_columns(columns: list[str]) -> dict[str, str]:
    lower = {c.strip().lower(): c for c in columns}
    found = {}
    for target, names in ALIASES.items():
        for name in names:
            if name in lower:
                found[target] = lower[name]
                break
    return found


def clean_sql(path: str | Path, con: duckdb.DuckDBPyConnection, **override: str) -> str:
    """SELECT that maps a file onto meter_id, ts, kwh (plus the raw kwh text, for profiling)."""
    src = source_sql(path)
    columns = [row[0] for row in con.execute(f"DESCRIBE SELECT * FROM {src}").fetchall()]
    cols = find_columns(columns) | {k: v for k, v in override.items() if v}
    missing = {"meter_id", "ts", "kwh"} - cols.keys()
    if missing:
        raise ValueError(f"can't find columns {sorted(missing)} in {columns}; pass them explicitly")
    return (
        f'SELECT CAST("{cols["meter_id"]}" AS VARCHAR) AS meter_id, '
        f'TRY_CAST("{cols["ts"]}" AS TIMESTAMP) AS ts, '
        f'TRY_CAST(TRIM(CAST("{cols["kwh"]}" AS VARCHAR)) AS DOUBLE) AS kwh, '
        f'CAST("{cols["kwh"]}" AS VARCHAR) AS raw_kwh '
        f"FROM {src}"
    )


def connect() -> duckdb.DuckDBPyConnection:
    con = duckdb.connect()
    con.execute("SET TimeZone = 'UTC'")
    return con


def read_readings(path: str | Path, naive_tz: str = "UTC", **override: str) -> pd.DataFrame:
    """Clean readings as a DataFrame. Naive timestamps are read as `naive_tz` (check the data!)."""
    con = connect()
    df = con.execute(f"SELECT meter_id, ts, kwh FROM ({clean_sql(path, con, **override)})").df()
    ts = pd.to_datetime(df["ts"])
    if ts.dt.tz is None:
        ts = ts.dt.tz_localize(naive_tz, ambiguous="NaT", nonexistent="NaT")
    df["ts"] = ts.dt.tz_convert("UTC")
    return df.dropna(subset=["ts"]).sort_values(["meter_id", "ts"], ignore_index=True)


def load_default() -> tuple[pd.DataFrame, str]:
    """Processed real data when the data role has produced it, otherwise the synthetic sample."""
    real = config.PROCESSED_DIR / "readings.parquet"
    if real.exists():
        return read_readings(real), "real"
    return read_readings(config.SAMPLE_DIR / "readings.parquet"), "sample"


def load_labels(source: str) -> pd.DataFrame | None:
    path = (config.SAMPLE_DIR if source == "sample" else config.PROCESSED_DIR) / "labels.csv"
    return pd.read_csv(path) if path.exists() else None
