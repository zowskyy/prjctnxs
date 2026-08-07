#!/usr/bin/env bash
# Minimal native / GPU VM smoke test for the frontier-syntax submodule.
# Run on a machine with Rust + (optional) NVIDIA GPU before release.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SUBMODULE="${ROOT}/external/frontier-syntax"
# Pin documented in README — main may not build release `frontier` binary yet.
EXPECTED_PIN="3db369c529c4c1a1b996fe44cfd4b5fd5e5a9ab3"

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
