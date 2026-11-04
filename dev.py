"""Team entry point: `uv run dev.py <command>`. Works the same on Windows and macOS.

run           API and UI on this task's ports (Emdash sets EMDASH_PORT per task)
smoke         the one check: lint, tests, API and UI boot, eval table
eval          write evals/results/latest.md
profile PATH  short profile of a dataset (see scripts/profile_data.py for flags)
synth         regenerate data/sample/
fetch NAME    download a practice dataset (london or uci) into DATA_DIR/raw
sync-skills   copy .agents/skills to .claude/skills
"""

from __future__ import annotations

import os
import subprocess
import sys
import time

import httpx

from common import config

PY = sys.executable


def start_api(port: int) -> subprocess.Popen:
    args = [PY, "-m", "uvicorn", "api.main:app", "--host", "127.0.0.1", "--port", str(port)]
    return subprocess.Popen(args, cwd=config.ROOT)


def start_ui(port: int, api_port: int) -> subprocess.Popen:
    args = [
        PY, "-m", "streamlit", "run", "ui/app.py",
        "--server.headless", "true",
        # Localhost only: on hackathon wifi, 0.0.0.0 would show the app to the whole room.
        "--server.address", "127.0.0.1",
        "--server.port", str(port),
        "--browser.gatherUsageStats", "false",
    ]  # fmt: skip
    env = os.environ | {"API_URL": f"http://127.0.0.1:{api_port}"}
    return subprocess.Popen(args, cwd=config.ROOT, env=env)


def wait_for(url: str, seconds: int = 90) -> bool:
    deadline = time.time() + seconds
    while time.time() < deadline:
        try:
            if httpx.get(url, timeout=5).status_code == 200:
                return True
        except httpx.HTTPError:
            pass
        time.sleep(1)
    return False


def stop(*procs: subprocess.Popen) -> None:
    for p in procs:
        p.terminate()
    for p in procs:
        try:
            p.wait(timeout=10)
        except subprocess.TimeoutExpired:
            p.kill()


def run() -> None:
    api, ui = start_api(config.API_PORT), start_ui(config.UI_PORT, config.API_PORT)
    print(f"API http://127.0.0.1:{config.API_PORT}/docs · UI http://127.0.0.1:{config.UI_PORT}")
    try:
        ui.wait()
    except KeyboardInterrupt:
        pass
    finally:
        stop(api, ui)


def smoke() -> int:
    from contract.schema import AnomalyList, ExplainResponse, Health

    results: list[tuple[str, bool, str]] = []

    def step(name: str, ok: bool, detail: str = "") -> None:
        results.append((name, ok, detail))
        print(f"[{'OK' if ok else 'FAIL'}] {name} {detail}".rstrip(), flush=True)

    step("ruff", subprocess.call([PY, "-m", "ruff", "check", "."], cwd=config.ROOT) == 0)
    step("pytest", subprocess.call([PY, "-m", "pytest"], cwd=config.ROOT) == 0)

    # Ports +5/+6 so smoke runs next to a `dev.py run` in the same task.
    api_port, ui_port = config.API_PORT + 5, config.UI_PORT + 5
    api, ui = start_api(api_port), start_ui(ui_port, api_port)
    base = f"http://127.0.0.1:{api_port}"
    try:
        up = wait_for(f"{base}/health")
        step("api boots", up, base)
        if up:
            health = Health.model_validate(httpx.get(f"{base}/health").json())
            listing = AnomalyList.model_validate(httpx.get(f"{base}/anomalies?limit=10").json())
            step("GET /anomalies", len(listing.items) > 0, f"{len(listing.items)} items")
            first = listing.items[0].meter_id
            body = httpx.post(f"{base}/explain", json={"meter_id": first}, timeout=120).json()
            ExplainResponse.model_validate(body)
            step("POST /explain", True, f"{first} via {health.llm}, data: {health.source}")
        step("ui boots", wait_for(f"http://127.0.0.1:{ui_port}/_stcore/health"), f":{ui_port}")
    except Exception as error:  # noqa: BLE001
        step("api contract", False, repr(error))
    finally:
        stop(api, ui)

    from evals import run as evals

    try:
        evals.main()
        step("eval table", True, "evals/results/latest.md")
    except Exception as error:  # noqa: BLE001
        step("eval table", False, repr(error))

    failed = [name for name, ok, _ in results if not ok]
    print("SMOKE OK" if not failed else f"SMOKE FAILED: {', '.join(failed)}")
    return 1 if failed else 0


def main() -> int:
    # Windows consoles default to cp1252, which can't print Romanian diacritics.
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8")
    if len(sys.argv) < 2 or sys.argv[1] in {"-h", "--help", "help"}:
        print(__doc__)
        return 0
    command, rest = sys.argv[1], sys.argv[2:]
    if command == "run":
        run()
    elif command == "smoke":
        return smoke()
    elif command == "eval":
        from evals import run as evals

        evals.main()
    elif command == "profile":
        from scripts import profile_data

        profile_data.main(rest)
    elif command == "synth":
        from scripts import synth

        synth.main()
    elif command == "fetch":
        from scripts import fetch_practice_data

        fetch_practice_data.main(rest)
    elif command == "sync-skills":
        from scripts import sync_skills

        sync_skills.main()
    else:
        print(f"unknown command {command!r}\n{__doc__}")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
