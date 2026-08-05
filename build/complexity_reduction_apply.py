#!/usr/bin/env python3
"""Record MCPE complexity reduction changes applied to Project Nexus."""

from __future__ import annotations

import json
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "audit_reports"


def main() -> int:
    from complexity_audit import analyze, write_report

    data = analyze()
    data["applied_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    data["changes"] = [
        "build/validator.py — UnifiedValidator for structural + metric gates",
        "build/rust_bridge.py — FrontierBridge.execute() unified API",
        "verify modules import validator (frontier_v2, improve_v2, quantum_leap)",
        "engine/nexus-runtime — ECS + game loop (1024 Hz gate)",
        "cursor-app — Tauri 2 + CodeMirror IDE shell",
        "Cargo workspace + rust-toolchain.toml + GitHub Actions CI",
    ]

    write_report(data)
    md = REPORTS / "complexity_reduction_applied.md"
    lines = [
        "# MCPE Complexity Reduction — Applied",
        "",
        f"**Applied:** {data['applied_at']}",
        "",
        "## Changes",
        "",
    ]
    for c in data["changes"]:
        lines.append(f"- {c}")
    lines.extend(["", "## Power Preservation", ""])
    for k, v in data["power_preserved"].items():
        lines.append(f"- **{k}:** {v}")
    md.write_text("\n".join(lines) + "\n", encoding="utf-8")

    json_path = REPORTS / "complexity_reduction_applied.json"
    json_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    print(f"✅ Applied report: {md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
