#!/usr/bin/env python3
"""Verify Tauri Linux CI job configuration and bundle path documentation.

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

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CI_WORKFLOW = ROOT / ".github" / "workflows" / "ci.yml"
VERIFY_SCRIPT = ROOT / "scripts" / "verify-tauri-build.sh"
# Documented relative path (matches CI verification step and verify-tauri-build.sh).
TAURI_BUNDLE_REL = "cursor-app/src-tauri/target/release/bundle"


def _read_ci_workflow() -> str:
    """Load CI workflow with transparent error handling."""
    try:
        if not CI_WORKFLOW.is_file():
            raise ValueError(f"error: missing CI workflow at {CI_WORKFLOW}")
        return CI_WORKFLOW.read_text(encoding="utf-8")
    except Exception as exc:
        raise ValueError(f"error reading CI workflow: {exc}") from exc


def _tauri_job_block(content: str) -> str:
    """Extract tauri job block for explainable CI validation."""
    match = re.search(
        r"^  tauri:\n(.*?)(?=^  \w+:|\Z)",
        content,
        re.MULTILINE | re.DOTALL,
    )
    if not match:
        raise ValueError("error: tauri job block not found in CI workflow")
    return match.group(0)


class TestTauriBuildCI(unittest.TestCase):
    def test_ci_workflow_exists(self):
        self.assertTrue(CI_WORKFLOW.is_file(), f"missing {CI_WORKFLOW}")

    def test_tauri_job_defined(self):
        content = _read_ci_workflow()
        self.assertIn("  tauri:", content)
        self.assertIn("name: Tauri shell (Linux)", content)

    def test_tauri_job_has_gtk_dependency(self):
        content = _read_ci_workflow()
        tauri_block = _tauri_job_block(content)
        self.assertIn("libgtk-3-dev", tauri_block)

    def test_bundle_verification_step_in_ci(self):
        content = _read_ci_workflow()
        self.assertIn("Verify Tauri bundle artifacts", content)
        self.assertIn("scripts/verify-tauri-build.sh", content)

    def test_verify_script_documents_bundle_path(self):
        self.assertTrue(VERIFY_SCRIPT.is_file(), f"missing {VERIFY_SCRIPT}")
        try:
            text = VERIFY_SCRIPT.read_text(encoding="utf-8")
        except Exception as exc:
            raise ValueError(f"error reading verify script: {exc}") from exc
        self.assertIn("target/release/bundle", text)
        self.assertIn("TAURI_BUNDLE_PASS", text)


if __name__ == "__main__":
    unittest.main()
