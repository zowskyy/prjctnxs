#!/usr/bin/env python3
"""Collapse v1/v2/v3 versioned .frontier files into archive/."""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "archive"
SUFFIXES = ("_v1.frontier", "_v2.frontier", "_v3.frontier")


def collapse(dry_run: bool = False) -> list[str]:
    moved: list[str] = []
    for path in sorted(ROOT.rglob("*.frontier")):
        if "archive" in path.parts:
            continue
        if not any(path.name.endswith(s) for s in SUFFIXES):
            continue
        rel = path.relative_to(ROOT)
        target = ARCHIVE / rel
        if dry_run:
            print(f"  would archive: {rel} -> archive/{rel}")
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(path), str(target))
            print(f"  archived: {rel} -> archive/{rel}")
        moved.append(str(rel))
    return moved


def main() -> int:
    dry = "--dry-run" in sys.argv
    print("📦 Collapsing version stack...")
    moved = collapse(dry_run=dry)
    if not moved:
        print("  (no versioned files found)")
    else:
        print(f"✅ {len(moved)} file(s) {'would be ' if dry else ''}archived")
    return 0


if __name__ == "__main__":
    sys.exit(main())
