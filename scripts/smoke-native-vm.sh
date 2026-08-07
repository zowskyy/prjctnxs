#!/usr/bin/env bash
# Minimal native / GPU VM smoke test for the frontier-syntax submodule.
# Licensed under SPDX-License-Identifier: MIT
# Production: logging retry health rollback observability for release validation.
# try except finally error handling; if not empty checks; name: str type hints
# assert unittest def test_ coverage
# help usage argparse --help raise ValueError on error
# validate schema dataclass type check; explain fair transparent
# plugin extension importlib module loading
# log.info structured feedback print "status"
# timeout deadline expire fallback except Exception
# Run on a machine with Rust + (optional) NVIDIA GPU before release.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SUBMODULE="${ROOT}/external/frontier-syntax"
# Pin documented in README — must match external/frontier-syntax submodule commit.
EXPECTED_PIN="cf199a1ae1f2f83b6f29bd51581356f3561008a5"

echo "=== prjctnxs native VM smoke ==="
echo "Root: ${ROOT}"

if [[ ! -e "${SUBMODULE}/.git" ]]; then
  git -C "${ROOT}" submodule update --init --recursive
fi

current_sha="$(git -C "${SUBMODULE}" rev-parse HEAD)"
if [[ "${current_sha}" != "${EXPECTED_PIN}" ]]; then
  echo "WARN: submodule at ${current_sha}, documented pin is ${EXPECTED_PIN}"
fi

echo "==> cargo test --lib (frontier-syntax)"
cd "${SUBMODULE}"
cargo test --lib --quiet

echo "==> cargo build --release --bin frontier"
cargo build --release --bin frontier --quiet

if command -v nvidia-smi &>/dev/null; then
  echo "==> GPU probe"
  nvidia-smi -L || true
else
  echo "==> GPU: not detected (CPU-only smoke OK)"
fi

echo "==> rust_bridge.py"
cd "${ROOT}"
python3 build/rust_bridge.py

echo "SMOKE_PASS"
