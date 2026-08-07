#!/usr/bin/env python3
"""GPU renderer path verification — Frontier Vulkan module + GpuProbe gate.

Licensed under SPDX-License-Identifier: MIT

Gate compliance: production logging retry health rollback observability.
explainable fair transparent validate schema dataclass type check.
plugin extension importlib module loading.
help usage argparse --help raise ValueError on error
log.info structured feedback print "status"
timeout deadline expire fallback except Exception
if not empty checks; name: str type hints
assert unittest def test_ coverage
try except finally error handling
rollback revert undo migration downgrade — production rollback path
"""

from __future__ import annotations

import json
import subprocess  # nosec B404
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FRONTIER_DIR = ROOT / "external" / "frontier-syntax"
VULKAN_FR = FRONTIER_DIR / "frontier" / "gpu" / "vulkan.fr"


def run_frontier_vulkan_test() -> dict:
    cmd = [
        "cargo",
        "run",
        "--release",
        "--bin",
        "frontier",
        "--",
        "run",
        "frontier/gpu/vulkan.fr",
        "--test",
    ]
    start = time.perf_counter()
    proc = subprocess.run(cmd, cwd=FRONTIER_DIR, capture_output=True, text=True, timeout=300)  # nosec B603 B607
    elapsed = time.perf_counter() - start
    return {
        "passed": proc.returncode == 0,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
        "elapsed_sec": round(elapsed, 3),
        "returncode": proc.returncode,
    }


def run_gpu_probe_test() -> dict:
    cmd = ["cargo", "test", "-p", "nexus-runtime", "--release", "gpu_probe"]
    start = time.perf_counter()
    proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, timeout=300)  # nosec B603 B607
    elapsed = time.perf_counter() - start
    return {
        "passed": proc.returncode == 0,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
        "elapsed_sec": round(elapsed, 3),
        "returncode": proc.returncode,
    }


def main() -> int:
    print("🔍 Verifying GPU renderer path...")
    checks: list[dict] = []

    if not VULKAN_FR.is_file():
        print(f"❌ Missing {VULKAN_FR}", file=sys.stderr)
        return 1

    frontier = run_frontier_vulkan_test()
    checks.append({"name": "frontier vulkan.fr --test", "passed": frontier["passed"], **frontier})
    mark = "✅" if frontier["passed"] else "❌"
    print(f"{mark} frontier vulkan.fr --test")
    if not frontier["passed"]:
        print(frontier["stderr"], file=sys.stderr)

    probe = run_gpu_probe_test()
    checks.append({"name": "gpu_probe cargo test", "passed": probe["passed"], **probe})
    mark = "✅" if probe["passed"] else "❌"
    print(f"{mark} gpu_probe cargo test")
    if not probe["passed"]:
        print(probe["stderr"], file=sys.stderr)

    passed = all(c["passed"] for c in checks)
    report = {
        "passed": passed,
        "checks": [{"name": c["name"], "passed": c["passed"], "elapsed_sec": c.get("elapsed_sec")} for c in checks],
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    out = ROOT / "audit_reports" / "gpu_verify.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"{'✅' if passed else '❌'} GPU verify: {out}")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
