#!/usr/bin/env python3
"""Integration verification — workspace build, tests, and ARC gates."""

from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(cmd: list[str], cwd: Path | None = None, timeout: int = 600) -> tuple[bool, str]:
    proc = subprocess.run(cmd, cwd=cwd or ROOT, capture_output=True, text=True, timeout=timeout)
    out = proc.stdout + proc.stderr
    return proc.returncode == 0, out


def main() -> int:
    checks: list[dict] = []
    t0 = time.perf_counter()

    ok, out = run(["cargo", "test", "-p", "nexus-runtime", "--release"])
    checks.append({"name": "nexus-runtime tests", "passed": ok})

    ok, out = run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"])
    checks.append({"name": "python tests (43+)", "passed": ok})

    ok, _ = run([sys.executable, "build/runtime_verify.py"])
    checks.append({"name": "runtime ECS gate", "passed": ok})

    ok, _ = run([sys.executable, "build/arc_orchestrator.py", "--verify-real"], timeout=300)
    checks.append({"name": "real bridge verify", "passed": ok})

    ok, _ = run(["npm", "run", "build"], cwd=ROOT / "cursor-app")
    checks.append({"name": "IDE frontend build", "passed": ok})

    passed = all(c["passed"] for c in checks)
    report = {
        "passed": passed,
        "checks": checks,
        "duration_sec": round(time.perf_counter() - t0, 2),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    out_path = ROOT / "audit_reports" / "integration_verify.json"
    out_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    for c in checks:
        mark = "✅" if c["passed"] else "❌"
        print(f"{mark} {c['name']}")
    print(f"\n{'✅' if passed else '❌'} Integration verify ({report['duration_sec']}s)")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
