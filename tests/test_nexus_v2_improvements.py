#!/usr/bin/env python3
"""Tests for Project Nexus v2.0 comprehensive improvement patch."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ORCH = ROOT / "build" / "arc_orchestrator.py"

IMPROVEMENT_FILES = [
    "frontier/ai/neural_engine_v2.frontier",
    "frontier/ai/language_model_v2.frontier",
    "benchmark/spirits_within/rendering_v2.frontier",
    "frontier/core/compiler_v2.frontier",
    "src/security/security_v2.frontier",
    "cursor/src/ai/workflow_v2.frontier",
    "src/asset/network_v2.frontier",
]


class TestNexusV2Improvements(unittest.TestCase):
    def test_improvement_files_exist(self):
        for rel in IMPROVEMENT_FILES:
            path = ROOT / rel
            self.assertTrue(path.is_file(), f"missing {rel}")
            self.assertGreater(path.stat().st_size, 200)

    def test_improvements_verification_passes(self):
        proc = subprocess.run(
            [sys.executable, str(ORCH), "--verify-improvements"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("IMPROVEMENTS COMPLETE", proc.stdout)

    def test_improve_patch_command(self):
        proc = subprocess.run(
            [sys.executable, str(ORCH), "--patch", "improve-v2.0"],
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

    def test_slide_15_no_regression(self):
        proc = subprocess.run(
            [sys.executable, str(ORCH), "--slides", "15"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)

    def test_improvement_report_generated(self):
        report = ROOT / "audit_reports" / "nexus_v2_improvements_report.json"
        if not report.exists():
            subprocess.run(
                [sys.executable, str(ORCH), "--verify-improvements"],
                cwd=ROOT,
                check=True,
            )
        data = json.loads(report.read_text(encoding="utf-8"))
        self.assertTrue(data["passed"])
        self.assertEqual(data["improvements"], 7)
        self.assertGreaterEqual(data["metrics"]["neural_fps"], 500)


if __name__ == "__main__":
    unittest.main()
