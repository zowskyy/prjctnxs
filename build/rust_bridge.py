#!/usr/bin/env python3
"""
Rust Bridge — Connects Project Nexus to the frontier-syntax Rust implementation.

Provides real builds, tests, parsing, WASM compilation, and timed measurements.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REPO = ROOT / "external" / "frontier-syntax"

WASM_MAGIC = b"\x00asm"


class RustBridge:
    """Bridge to frontier-syntax (Rust crate `frontier`, binary `frontier`)."""

    def __init__(self, repo_path: Path | None = None):
        self.repo_path = (repo_path or DEFAULT_REPO).resolve()
        self._binary: Path | None = None

    def ensure_repo(self) -> None:
        if not self.repo_path.exists():
            raise FileNotFoundError(
                f"frontier-syntax not found at {self.repo_path}. "
                "Run: git submodule update --init --recursive"
            )
        if not (self.repo_path / "Cargo.toml").exists():
            raise FileNotFoundError(f"Invalid frontier-syntax checkout at {self.repo_path}")

    @property
    def binary(self) -> Path:
        if self._binary is not None:
            return self._binary
        release = self.repo_path / "target" / "release" / "frontier"
        debug = self.repo_path / "target" / "debug" / "frontier"
        if release.exists():
            self._binary = release
        elif debug.exists():
            self._binary = debug
        else:
            self._binary = release
        return self._binary

    def build(self, release: bool = True) -> bool:
        self.ensure_repo()
        profile = ["--release"] if release else []
        print("🔨 Building frontier-syntax...")
        result = subprocess.run(
            ["cargo", "build", *profile],
            cwd=self.repo_path,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            print("❌ Build failed:", result.stderr[-2000:])
            return False
        self._binary = None
        print("✅ Build successful")
        return True

    def run_cargo_test(self, test_filter: str = "") -> tuple[bool, str, float]:
        """Run cargo test --lib; return success, output, wall_seconds."""
        self.ensure_repo()
        cmd = ["cargo", "test", "--lib"]
        if test_filter:
            cmd.extend([test_filter, "--", "--nocapture"])
        start = time.perf_counter()
        result = subprocess.run(cmd, cwd=self.repo_path, capture_output=True, text=True)
        elapsed = time.perf_counter() - start
        output = result.stdout + result.stderr
        return result.returncode == 0, output, elapsed

    def run_test(self, test_name: str) -> tuple[bool, str]:
        ok, output, _ = self.run_cargo_test(test_name)
        return ok, output

    def parse_v2(self, source_path: Path) -> tuple[bool, str]:
        self.ensure_repo()
        if not self.binary.exists() and not self.build():
            return False, "frontier binary not built"
        result = subprocess.run(
            [str(self.binary), "parse-v2", str(source_path)],
            cwd=self.repo_path,
            capture_output=True,
            text=True,
        )
        return result.returncode == 0, result.stdout + result.stderr

    def compile_to_wasm(self, source_path: Path, output_path: Path | None = None) -> tuple[bool, bytes | str]:
        """Compile .fr source to WASM bytes."""
        self.ensure_repo()
        if not self.binary.exists() and not self.build():
            return False, "frontier binary not built"

        out = output_path or Path(tempfile.mkstemp(suffix=".wasm")[1])
        result = subprocess.run(
            [
                str(self.binary),
                "compile",
                str(source_path),
                "--target",
                "wasm",
                "-o",
                str(out),
            ],
            cwd=self.repo_path,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            return False, result.stderr or result.stdout
        data = out.read_bytes()
        if not data.startswith(WASM_MAGIC):
            return False, "output is not valid WASM"
        return True, data

    def compile_frontier(self, source: str, suffix: str = ".fr") -> tuple[bool, bytes | str]:
        """Write source to a temp file and compile to WASM."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=suffix, delete=False, encoding="utf-8") as f:
            f.write(source)
            temp_path = Path(f.name)
        wasm_out = temp_path.with_suffix(".wasm")
        try:
            return self.compile_to_wasm(temp_path, wasm_out)
        finally:
            temp_path.unlink(missing_ok=True)
            wasm_out.unlink(missing_ok=True)

    def run_binary(self, binary: bytes) -> tuple[bool, str]:
        """Validate WASM module magic (full WASM execution requires wasmtime)."""
        if binary[:4] == WASM_MAGIC:
            return True, f"valid WASM module ({len(binary)} bytes)"
        return False, "invalid WASM magic"

    def measure_parse_throughput(self, iterations: int = 5000) -> dict[str, Any]:
        """Measure parser fuzz throughput via frontier fuzz CLI."""
        self.ensure_repo()
        if not self.binary.exists() and not self.build():
            return {"error": "build failed", "measured": False}

        start = time.perf_counter()
        result = subprocess.run(
            [str(self.binary), "fuzz", str(iterations)],
            cwd=self.repo_path,
            capture_output=True,
            text=True,
        )
        elapsed = time.perf_counter() - start
        if result.returncode != 0:
            return {"error": result.stderr, "measured": False}

        parsed_per_sec = iterations / elapsed if elapsed > 0 else 0.0
        return {
            "measured": True,
            "iterations": iterations,
            "elapsed_sec": round(elapsed, 4),
            "parse_per_sec": round(parsed_per_sec, 1),
            "stdout": result.stdout.strip(),
        }

    def measure_neural_completion(self) -> dict[str, Any]:
        """Run neural completion unit tests and time them."""
        ok, output, elapsed = self.run_cargo_test("test_neural_suggestions")
        return {
            "measured": ok,
            "tests_passed": ok,
            "elapsed_sec": round(elapsed, 4),
            "neural_tests": 1,
            "detail": "neural::completion::test_neural_suggestions",
        }

    def measure_cargo_test_suite(self) -> dict[str, Any]:
        """Run full lib test suite and return counts + timing."""
        ok, output, elapsed = self.run_cargo_test("")
        passed = output.count("test result: ok")
        return {
            "measured": ok,
            "elapsed_sec": round(elapsed, 4),
            "suite_passed": ok,
            "detail": "cargo test --lib",
        }

    def health_check(self) -> dict[str, Any]:
        self.ensure_repo()
        built = self.binary.exists() or self.build()
        test_ok, _, test_sec = self.run_cargo_test("test_v2_pipeline")
        return {
            "repo_path": str(self.repo_path),
            "binary": str(self.binary),
            "built": built,
            "binary_exists": self.binary.exists(),
            "v2_pipeline_test": test_ok,
            "test_elapsed_sec": round(test_sec, 4),
        }


_bridge: RustBridge | None = None


def get_bridge(repo_path: Path | None = None) -> RustBridge:
    global _bridge
    if _bridge is None or (repo_path is not None and repo_path != _bridge.repo_path):
        _bridge = RustBridge(repo_path)
    return _bridge


def main() -> int:
    bridge = get_bridge()
    try:
        health = bridge.health_check()
    except FileNotFoundError as e:
        print(f"❌ {e}")
        return 1
    print(json.dumps(health, indent=2))
    return 0 if health.get("built") and health.get("v2_pipeline_test") else 1


if __name__ == "__main__":
    sys.exit(main())
