"""Short markdown profile of a readings file or folder, computed in DuckDB.

Safe to paste into an agent's context: it prints counts and at most 5 rows, never the data.
"""

from __future__ import annotations

import argparse

from common import config
from ml.load import clean_sql, connect


def profile(path: str, tz: str = config.TIMEZONE, **override: str) -> str:
    con = connect()
    con.execute(f"CREATE TEMP VIEW r AS {clean_sql(path, con, **override)}")
    q = lambda sql: con.execute(sql).fetchall()  # noqa: E731

    rows, meters, bad_ts, t0, t1 = q(
        "SELECT count(*), count(DISTINCT meter_id), count(*) FILTER (ts IS NULL), "
        "min(ts), max(ts) FROM r"
    )[0]
    nulls, null_text, other_text, zeros, negatives = q(
        "SELECT count(*) FILTER (kwh IS NULL), "
        "count(*) FILTER (kwh IS NULL AND upper(trim(raw_kwh)) IN ('NULL', 'NAN', 'NA', '')), "
        "count(*) FILTER (kwh IS NULL AND raw_kwh IS NOT NULL "
        "  AND upper(trim(raw_kwh)) NOT IN ('NULL', 'NAN', 'NA', '')), "
        "count(*) FILTER (kwh = 0), count(*) FILTER (kwh < 0) FROM r"
    )[0]
    steps = q(
        "SELECT step, count(*) n FROM (SELECT ts - lag(ts) OVER (PARTITION BY meter_id ORDER BY ts)"
        " AS step FROM r) WHERE step IS NOT NULL GROUP BY step ORDER BY n DESC LIMIT 4"
    )
    per_day = q(
        "SELECT n, count(*) AS n_days FROM (SELECT meter_id, "
        f"CAST(timezone('{tz}', ts::TIMESTAMPTZ) AS DATE) AS d, count(*) AS n FROM r "
        "WHERE ts IS NOT NULL GROUP BY ALL) GROUP BY n ORDER BY n_days DESC LIMIT 6"
    )
    dupes = q("SELECT count(*) - count(DISTINCT (meter_id, ts)) FROM r")[0][0]
    counters = q(
        "SELECT meter_id FROM (SELECT meter_id, "
        "kwh - lag(kwh) OVER (PARTITION BY meter_id ORDER BY ts) dk FROM r) "
        "GROUP BY meter_id "
        "HAVING count(dk) > 10 AND avg(CASE WHEN dk >= 0 THEN 1 ELSE 0 END) > 0.99"
    )
    head = q("SELECT meter_id, ts, raw_kwh FROM r ORDER BY meter_id, ts LIMIT 5")

    pct = lambda n: f"{n:,} ({n / rows:.1%})" if rows else "0"  # noqa: E731
    lines = [
        f"# Profile: {path}",
        f"- rows: {rows:,} · meters: {meters:,} · unparsed timestamps: {bad_ts:,}",
        f"- time range (as read, UTC if naive): {t0} to {t1}",
        "- steps between readings: " + ", ".join(f"{s} ×{n:,}" for s, n in steps),
        f"- readings per local day ({tz}): " + ", ".join(f"{n} ×{d:,}" for n, d in per_day),
        f"- kwh missing: {pct(nulls)}; of which 'Null'/'NaN' text: {null_text:,}; "
        f"other unparsed text: {other_text:,}",
        f"- kwh zero: {pct(zeros)} · negative: {negatives:,}",
        f"- duplicate (meter, ts) rows: {dupes:,}",
        f"- meters that only go up (cumulative counters?): {len(counters)}"
        + (f" → {', '.join(m for (m,) in counters[:10])}" if counters else ""),
        "",
        "| meter_id | ts | raw kwh |",
        "| --- | --- | --- |",
        *[f"| {m} | {t} | {k} |" for m, t, k in head],
    ]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path")
    parser.add_argument("--id", dest="meter_id")
    parser.add_argument("--ts")
    parser.add_argument("--value", dest="kwh")
    parser.add_argument("--tz", default=config.TIMEZONE)
    args = parser.parse_args(argv)
    print(profile(args.path, args.tz, meter_id=args.meter_id, ts=args.ts, kwh=args.kwh))


if __name__ == "__main__":
    main()
