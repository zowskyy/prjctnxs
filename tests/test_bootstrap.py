#!/usr/bin/env python3
"""Bootstrap verification tests for Project Nexus v3.0 workspace."""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "build"))


class TestWorkspaceBootstrap(unittest.TestCase):
    def test_cargo_workspace_exists(self):
        self.assertTrue((ROOT / "Cargo.toml").is_file())
        self.assertTrue((ROOT / "engine/nexus-runtime/Cargo.toml").is_file())

    def test_rust_toolchain(self):
        self.assertTrue((ROOT / "rust-toolchain.toml").is_file())

    def test_cursor_app_package(self):
        self.assertTrue((ROOT / "cursor-app/package.json").is_file())

    def test_ci_workflow(self):
        self.assertTrue((ROOT / ".github/workflows/ci.yml").is_file())

    def test_unified_validator(self):
        from validator import UnifiedValidator, MCPE_METRIC_FLOORS

        v = UnifiedValidator()
        self.assertGreaterEqual(MCPE_METRIC_FLOORS["neural_fps"], 1000)
        ok, found, total = v.verify_structural(
            "frontier/ai/neural_engine.frontier",
            ["component Tensor"],
        )
        self.assertTrue(ok, f"markers {found}/{total}")

    def test_bridge_execute_api(self):
        from rust_bridge import FrontierBridge, get_bridge

        bridge = get_bridge()
        self.assertIsInstance(bridge, FrontierBridge)
        health = bridge.execute("health")
        self.assertIn("repo_path", health)

    def test_nexus_runtime_bench(self):
        proc = subprocess.run(
            ["cargo", "run", "--release", "-p", "nexus-runtime", "--bin", "nexus-bench", "--", "10000"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=120,
        )
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("ARC gate: PASS", proc.stdout)


if __name__ == "__main__":
    unittest.main()
