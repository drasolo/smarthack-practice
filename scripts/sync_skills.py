"""Copy .agents/skills/ (read by Codex and Antigravity) to .claude/skills/ (read by Claude Code)."""

from __future__ import annotations

import shutil

from common import config


def main() -> None:
    source = config.ROOT / ".agents" / "skills"
    target = config.ROOT / ".claude" / "skills"
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(source, target)
    names = sorted(p.name for p in target.iterdir() if p.is_dir())
    print(f"synced {len(names)} skills to .claude/skills: {', '.join(names)}")


if __name__ == "__main__":
    main()
