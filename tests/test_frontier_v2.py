#!/usr/bin/env python3
"""Tests for Frontier v2.0 patch integration."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ORCH = ROOT / "build" / "arc_orchestrator.py"


class TestFrontierV2(unittest.TestCase):
    def test_core_modules_exist(self):
        core = [
            "frontier/core/parser.frontier",
            "frontier/core/types.frontier",
            "frontier/core/memory.frontier",
            "frontier/core/concurrency.frontier",
            "frontier/core/errors.frontier",
            "frontier/core/stdlib.frontier",
            "frontier/core/compiler.frontier",
        ]
        for rel in core:
            path = ROOT / rel
            self.assertTrue(path.is_file(), f"missing {rel}")
            self.assertGreater(path.stat().st_size, 100)

    def test_v2_innovation_modules_exist(self):
        innovations = [
            "frontier/grammar/mutator.frontier",
            "src/security/proof_carrying.frontier",
            "src/security/pq_signatures.frontier",
            "src/security/zk_snarks.frontier",
            "src/asset/ipfs_resolver.frontier",
            "src/asset/registry.frontier",
            "cursor/src/ai/completion.frontier",
            "cursor/src/ai/context.frontier",
            "cursor/src/ai/knowledge/hypercube.frontier",
        ]
        for rel in innovations:
            self.assertTrue((ROOT / rel).is_file(), f"missing {rel}")

    def test_syntax_artifacts_exist(self):
        artifacts = [
            "frontier/syntax/Frontier.g4",
            "frontier/syntax/feature_matrix_v2.json",
            "frontier/syntax/schema_v2.json",
            "frontier/syntax/grammar_v2.json",
            "frontier/syntax/ast_sample_v2.json",
            "frontier/syntax/ast_hash_v2.sha3",
            "frontier/syntax/final_hash_v2.sha3",
        ]
        for rel in artifacts:
            self.assertTrue((ROOT / rel).exists(), f"missing {rel}")

    def test_v2_verification_passes(self):
        proc = subprocess.run(
            [sys.executable, str(ORCH), "--verify"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("FRONTIER V2.0 VERIFIED", proc.stdout)

    def test_slide_15_no_regression(self):
        proc = subprocess.run(
            [sys.executable, str(ORCH), "--slides", "15"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("SLIDE 15 PASSED", proc.stdout)

    def test_v2_report_generated(self):
        report = ROOT / "audit_reports" / "frontier_v2_report.json"
        if not report.exists():
            subprocess.run([sys.executable, str(ORCH), "--verify"], cwd=ROOT, check=True)
        data = json.loads(report.read_text(encoding="utf-8"))
        self.assertTrue(data["passed"])
        self.assertEqual(data["innovations"], 7)


if __name__ == "__main__":
    unittest.main()
