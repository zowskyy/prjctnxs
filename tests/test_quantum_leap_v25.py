#!/usr/bin/env python3
"""Tests for Project Nexus v2.5 Quantum Leap patch."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ORCH = ROOT / "build" / "arc_orchestrator.py"

V3_FILES = [
    "frontier/ai/neural_engine_v3.frontier",
    "frontier/ai/language_model_v3.frontier",
    "benchmark/spirits_within/rendering_v3.frontier",
    "frontier/core/compiler_v3.frontier",
    "src/security/security_v3.frontier",
    "src/asset/network_v3.frontier",
    "benchmark/spirits_within/final_fantasy_visualizer_ultra.frontier",
]


class TestQuantumLeapV25(unittest.TestCase):
    def test_v3_modules_exist(self):
        for rel in V3_FILES:
            path = ROOT / rel
            self.assertTrue(path.is_file(), f"missing {rel}")
            self.assertGreater(path.stat().st_size, 200)

    def test_quantum_leap_verification_passes(self):
        proc = subprocess.run(
            [sys.executable, str(ORCH), "--verify-quantum-leap"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("QUANTUM LEAP VERIFICATION COMPLETE", proc.stdout)
        self.assertIn("ALL DOUBLED ARC GATES PASSED", proc.stdout)

    def test_quantum_leap_patch_command(self):
        proc = subprocess.run(
            [sys.executable, str(ORCH), "--patch", "quantum-leap-v2.5"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)

    def test_v2_improvements_still_pass(self):
        proc = subprocess.run(
            [sys.executable, str(ORCH), "--verify-improvements"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)

    def test_v2_base_still_passes(self):
        proc = subprocess.run(
            [sys.executable, str(ORCH), "--verify"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)

    def test_quantum_leap_report_generated(self):
        report = ROOT / "audit_reports" / "nexus_v25_quantum_leap_report.json"
        if not report.exists():
            subprocess.run(
                [sys.executable, str(ORCH), "--verify-quantum-leap"],
                cwd=ROOT,
                check=True,
            )
        data = json.loads(report.read_text(encoding="utf-8"))
        self.assertTrue(data["passed"])
        self.assertEqual(data["modules"], 7)
        self.assertGreaterEqual(data["metrics"]["fps"], 1000)
        self.assertGreaterEqual(data["metrics"]["render_fps"], 240)


if __name__ == "__main__":
    unittest.main()
