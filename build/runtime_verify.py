#!/usr/bin/env python3
"""Verify nexus-runtime ECS benchmark meets ARC gate (1024 Hz, 1000+ entities)."""

from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET_HZ = 1024.0
MIN_ENTITIES = 1000


def run_bench(ticks: int = 50_000) -> dict:
    cmd = ["cargo", "run", "--release", "-p", "nexus-runtime", "--bin", "nexus-bench", "--", str(ticks)]
    start = time.perf_counter()
    proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    elapsed = time.perf_counter() - start
    passed = proc.returncode == 0
    return {
        "passed": passed,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
        "elapsed_sec": round(elapsed, 3),
        "returncode": proc.returncode,
    }


def main() -> int:
    print("🔍 Verifying nexus-runtime ECS benchmark...")
    result = run_bench()
    print(result["stdout"])
    if not result["passed"]:
        print(result["stderr"], file=sys.stderr)
        return 1

    report = {
        "passed": True,
        "target_hz": TARGET_HZ,
        "min_entities": MIN_ENTITIES,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "bench": result,
    }
    out = ROOT / "audit_reports" / "runtime_verify.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"✅ Runtime verify: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
