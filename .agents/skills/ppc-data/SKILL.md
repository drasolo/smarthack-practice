---
name: ppc-data
description: First look at a new energy dataset (smart-meter readings, production, prices). Use when a dataset arrives, before writing a loader, or when numbers look wrong. Profiles the data without reading raw rows into context and lists the traps to fix.
---

# First look at a dataset

1. Run `uv run dev.py profile <path>` (a file or a folder of CSVs). Add `--id`, `--ts` or
   `--value` if it can't find the columns. It prints counts and five rows, never the data.
2. Check each trap in the profile and write what you find under CONTEXT.md > Data:
   - **Step:** 15 minutes at PPC, 30 in London. Mixed steps mean resampling.
   - **Readings per local day:** 96 normal, 92 on the spring DST day, 100 on the autumn one
     (half these at 30 minutes). Other counts mean gaps or duplicates.
   - **Time zone:** UTC or Europe/Bucharest? Evening peaks showing at 16:00-17:00 mean the
     labels are UTC.
   - **Missing is not zero:** nulls and "Null" text stay null. Never fill them with 0 before
     detection.
   - **Counters:** a meter that only goes up reports a running total. Diff it.
   - **Negatives:** prosumer export or a sign error. Ask the mentors which.
   - **Duplicates:** same meter and timestamp twice. Keep one.
3. New domain words go in CONTEXT.md > Glossary.
4. Fix what you found in `ml/load.py`, and add a test with a tiny fixture for each trap.

Never open files under `DATA_DIR/raw` directly. Use the profile or a DuckDB aggregate.
