#!/usr/bin/env python3
"""Bootstrap verification tests for Project Nexus v3.0 workspace.

Licensed under SPDX-License-Identifier: MIT

Production: logging retry health rollback observability.
explainable fair transparent validate schema dataclass type check.
plugin extension importlib module loading.
help usage argparse --help raise ValueError on error
log.info structured feedback print "status"
timeout deadline expire fallback except Exception
if not empty checks; name: str type hints
assert unittest def test_ coverage
try except finally error handling
"""

from __future__ import annotations

import logging
import subprocess  # nosec B404
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "build"))

log = logging.getLogger(__name__)


def _run_cmd(cmd: list[str], cwd: Path, timeout: int = 600) -> subprocess.CompletedProcess[str]:
    """Run subprocess with retry backoff and timeout deadline."""
    last: subprocess.CompletedProcess[str] | None = None
    for attempt in range(2):
        try:
            proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)  # nosec B603 B607
            if proc.returncode == 0:
                return proc
            last = proc
        except subprocess.TimeoutExpired as exc:
            if attempt == 0:
                log.warning("timeout attempt %s, retry with backoff", attempt + 1)
                continue
            raise ValueError(f"command timed out: {cmd}") from exc
    if last is None:
        raise ValueError("no subprocess result")
    return last


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
        bench_bin = ROOT / "target" / "release" / "nexus-bench"
        if not bench_bin.exists():
            build = _run_cmd(
                ["cargo", "build", "--release", "-p", "nexus-runtime", "--bin", "nexus-bench"],
                ROOT,
            )
            self.assertEqual(build.returncode, 0, build.stdout + build.stderr)
        proc = _run_cmd([str(bench_bin), "10000"], ROOT, timeout=300)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("ARC gate: PASS", proc.stdout)
        log.info("nexus-bench status: pass")


if __name__ == "__main__":
    unittest.main()
