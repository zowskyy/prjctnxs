#!/usr/bin/env python3
"""Behavioral tests for the real implementation bridge."""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ORCH = ROOT / "build" / "arc_orchestrator.py"

sys.path.insert(0, str(ROOT / "build"))


class TestRustBridge(unittest.TestCase):
    def test_submodule_exists(self):
        path = ROOT / "external" / "frontier-syntax" / "Cargo.toml"
        self.assertTrue(path.is_file(), "external/frontier-syntax submodule missing")

    def test_bridge_health(self):
        from rust_bridge import get_bridge

        bridge = get_bridge()
        health = bridge.health_check()
        self.assertTrue(health["binary_exists"])
        self.assertTrue(health["v2_pipeline_test"])


class TestVerticalSlice(unittest.TestCase):
    def test_addition(self):
        from vertical_slice import run_vertical_slice

        self.assertTrue(run_vertical_slice("Create a function that adds two numbers", verbose=False))

    def test_hello_world(self):
        from vertical_slice import run_vertical_slice

        self.assertTrue(run_vertical_slice("Print hello world", verbose=False))

    def test_fibonacci(self):
        from vertical_slice import run_vertical_slice

        self.assertTrue(run_vertical_slice("Calculate fibonacci of 10", verbose=False))


class TestRealMetrics(unittest.TestCase):
    def test_metrics_are_measured(self):
        from real_benchmarks import get_real_metrics

        metrics = get_real_metrics()
        self.assertEqual(metrics["source"], "measured")
        self.assertTrue(metrics["bridge_available"])
        self.assertNotEqual(metrics.get("parse_per_sec", 0), 0)

    def test_metrics_not_structural_fallback(self):
        from real_benchmarks import STRUCTURAL_FALLBACK, get_real_metrics

        metrics = get_real_metrics()
        if metrics["source"] == "measured":
            self.assertNotEqual(metrics.get("parse_per_sec"), STRUCTURAL_FALLBACK["parse_per_sec"])


class TestVerifyReal(unittest.TestCase):
    def test_verify_real_orchestrator(self):
        proc = subprocess.run(
            [sys.executable, str(ORCH), "--verify-real"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=300,
        )
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("REAL IMPLEMENTATION BRIDGE COMPLETE", proc.stdout)


class TestVersionCollapse(unittest.TestCase):
    def test_v2_v3_archived(self):
        archived = ROOT / "archive" / "frontier" / "ai" / "neural_engine_v3.frontier"
        self.assertTrue(archived.is_file())
        live = ROOT / "frontier" / "ai" / "neural_engine_v3.frontier"
        self.assertFalse(live.exists())

    def test_base_modules_remain(self):
        self.assertTrue((ROOT / "frontier" / "ai" / "neural_engine.frontier").is_file())


if __name__ == "__main__":
    unittest.main()
