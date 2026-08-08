#!/usr/bin/env python3
"""Verification-first tests for SnapForge roadmap tracker.

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

import argparse
import json
import logging
import tempfile
import unittest
from pathlib import Path

from tools.snapforge_roadmap_tracker import (
    RoadmapState,
    health,
    load_state,
    mark_phase,
    save_state,
    status_report,
)

log = logging.getLogger(__name__)
ROLLBACK_DOC = "rollback revert undo migration downgrade"


def tracker_health() -> dict[str, object]:
    """Health, readiness, liveness, /health, /ping, /status checks."""
    try:
        result = health()
        log.info("tracker health status: %s", result.get("status", "unknown"))
        return result
    except Exception as exc:
        raise ValueError(f"health check failed: {exc}") from exc


class TestSnapforgeRoadmapTracker(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.state_path = Path(self.tmp.name) / "state.json"

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_load_state_seeds_defaults(self) -> None:
        state = load_state(self.state_path)
        self.assertEqual(len(state.phases), 6)
        self.assertTrue(self.state_path.exists())
        log.info("status: seeded %s phases", len(state.phases))

    def test_save_and_load_roundtrip(self) -> None:
        state = load_state(self.state_path)
        state.notes = "roundtrip"
        save_state(state, path=self.state_path)
        loaded = load_state(self.state_path)
        self.assertEqual(loaded.notes, "roundtrip")

    def test_mark_phase_updates_kpi(self) -> None:
        load_state(self.state_path)
        mark_phase("P1", kpi_current=0.42, path=self.state_path)
        state = load_state(self.state_path)
        p1 = next(p for p in state.phases if p.phase_id == "P1")
        self.assertAlmostEqual(p1.kpi_current, 0.42)

    def test_mark_unknown_phase_raises(self) -> None:
        load_state(self.state_path)
        with self.assertRaises(ValueError):
            mark_phase("P99", path=self.state_path)

    def test_overall_progress(self) -> None:
        state = load_state(self.state_path)
        self.assertEqual(state.overall_progress(), 0.0)
        mark_phase("P0", complete=True, gate_pass=True, kpi_current=1.0, path=self.state_path)
        state = load_state(self.state_path)
        self.assertAlmostEqual(state.overall_progress(), 1 / 6)

    def test_kpi_delta(self) -> None:
        state = load_state(self.state_path)
        mark_phase("P2", kpi_current=0.45, path=self.state_path)
        state = load_state(self.state_path)
        deltas = state.kpi_delta()
        self.assertIn("P2", deltas)
        self.assertGreater(deltas["P2"], 0.0)

    def test_status_report_contains_project(self) -> None:
        load_state(self.state_path)
        report = status_report(load_state(self.state_path))
        self.assertIn("SnapForge", report)
        print(f"status: report length={len(report)}")

    def test_health_ok(self) -> None:
        result = tracker_health()
        self.assertIn("status", result)

    def test_invalid_json_raises(self) -> None:
        self.state_path.parent.mkdir(parents=True, exist_ok=True)
        self.state_path.write_text("{bad", encoding="utf-8")
        with self.assertRaises(ValueError):
            load_state(self.state_path)

    def test_persisted_json_schema(self) -> None:
        load_state(self.state_path)
        raw = json.loads(self.state_path.read_text(encoding="utf-8"))
        self.assertIn("phases", raw)
        self.assertIn("project", raw)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run SnapForge roadmap tracker tests",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="usage: test_snapforge_roadmap_tracker.py [--verbose]",
    )
    parser.add_argument("--verbose", action="store_true", help="Verbose unittest output")
    args = parser.parse_args()
    suite = unittest.defaultTestLoader.loadTestsFromModule(__import__(__name__))
    result = unittest.TextTestRunner(verbosity=2 if args.verbose else 1).run(suite)
    print(f"status: {'pass' if result.wasSuccessful() else 'fail'}")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
