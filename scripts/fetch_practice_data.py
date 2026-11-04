"""Download a public practice dataset into DATA_DIR/raw/<name>/ and unzip it.

london: UK Power Networks "SmartMeter Energy Consumption Data in London Households",
        5,567 households, half-hourly, 2011-2014. About 800 MB zipped.
uci:    UCI ElectricityLoadDiagrams20112014, 370 clients, 15-minute, 2011-2014.
"""

from __future__ import annotations

import argparse
import zipfile

import httpx

from common import config

DATASETS = {
    "london": "https://data.london.gov.uk/download/smartmeter-energy-use-data-in-london-households/"
    "3527bf39-d93e-4071-8451-df2ade1ea4f2/Power-Networks-LCL-June2015(withAcorn).zip",
    "uci": "https://archive.ics.uci.edu/static/public/321/electricityloaddiagrams20112014.zip",
}


def fetch(name: str) -> None:
    target = config.RAW_DIR / name
    target.mkdir(parents=True, exist_ok=True)
    archive = target / f"{name}.zip"
    if not archive.exists():
        partial = archive.with_suffix(".part")
        headers = {"User-Agent": "smarthack-practice-fetch"}
        with httpx.stream(
            "GET", DATASETS[name], headers=headers, follow_redirects=True, timeout=60
        ) as r:
            r.raise_for_status()
            total = int(r.headers.get("content-length") or 0)
            done, next_report = 0, 0
            with open(partial, "wb") as f:
                for chunk in r.iter_bytes(1 << 20):
                    f.write(chunk)
                    done += len(chunk)
                    if done >= next_report:
                        size = f"{done >> 20} MB" + (f" of {total >> 20} MB" if total else "")
                        print(f"  {name}: {size}", flush=True)
                        next_report += 50 << 20
        partial.rename(archive)
    with zipfile.ZipFile(archive) as z:
        z.extractall(target)
    print(f"{name}: unzipped into {target}")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("name", choices=sorted(DATASETS))
    fetch(parser.parse_args(argv).name)


if __name__ == "__main__":
    main()
