#!/usr/bin/env python3
"""
Unified Validator — MCPE-aligned gate checking for Project Nexus.

Consolidates structural marker checks and metric gates used across all verify modules.
Power preservation: metrics must meet or exceed v2.5 Quantum Leap targets.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal

ROOT = Path(__file__).resolve().parents[1]

# v2.5 Quantum Leap minimum targets (MCPE — never regress)
MCPE_METRIC_FLOORS = {
    "neural_fps": 1000.0,
    "neural_accuracy": 0.99,
    "lm_latency_ms": 2.5,
    "lm_accuracy": 0.99,
    "render_fps": 240.0,
    "compiler_speedup": 200.0,
    "parse_per_sec": 1000.0,
    "network_replicas": 20,
}


@dataclass
class GateResult:
    name: str
    target: str
    measured: str
    passed: bool
    detail: str = ""


class UnifiedValidator:
    """Single entry point for structural and metric verification."""

    def __init__(self, root: Path | None = None):
        self.root = (root or ROOT).resolve()

    def resolve_path(self, rel_path: str) -> Path | None:
        path = self.root / rel_path
        if path.exists():
            return path
        archive = self.root / "archive" / rel_path
        if archive.exists():
            return archive
        return None

    def verify_structural(self, rel_path: str, markers: list[str]) -> tuple[bool, int, int]:
        path = self.resolve_path(rel_path)
        if path is None:
            return False, 0, len(markers)
        body = path.read_text(encoding="utf-8")
        found = sum(1 for m in markers if m in body)
        return found == len(markers), found, len(markers)

    def verify_metric(
        self,
        name: str,
        value: float,
        target: float,
        op: Literal[">=", "<=", "=="] = ">=",
    ) -> GateResult:
        if op == ">=":
            passed = value >= target
        elif op == "<=":
            passed = value <= target
        else:
            passed = value == target
        return GateResult(
            name=name,
            target=f"{op} {target}",
            measured=str(value),
            passed=passed,
        )

    def verify_mcpe_floor(self, metric: str, value: float) -> GateResult:
        floor = MCPE_METRIC_FLOORS.get(metric)
        if floor is None:
            return GateResult(metric, "defined", str(value), True, "no floor defined")
        if metric == "lm_latency_ms":
            return self.verify_metric(metric, value, floor, "<=")
        return self.verify_metric(metric, value, floor, ">=")

    def structural_gate(self, name: str, rel_path: str, markers: list[str]) -> GateResult:
        ok, found, total = self.verify_structural(rel_path, markers)
        return GateResult(
            name=name,
            target=f"`{rel_path}` ({total} markers)",
            measured=f"{found}/{total} markers",
            passed=ok,
            detail=str(self.resolve_path(rel_path) or "missing"),
        )


def verify_file_markers(rel_path: str, markers: list[str]) -> tuple[bool, int, int]:
    """Back-compat helper for existing verify modules."""
    return UnifiedValidator().verify_structural(rel_path, markers)
