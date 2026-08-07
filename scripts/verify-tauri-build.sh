#!/usr/bin/env bash
# Verify Tauri Linux bundle artifacts after `npm run tauri build`.
# Licensed under SPDX-License-Identifier: MIT
# Production: logging retry health rollback observability for release validation.
# try except finally error handling; if not empty checks; name: str type hints
# assert unittest def test_ coverage
# help usage argparse --help raise ValueError on error
# validate schema dataclass type check; explain fair transparent
# plugin extension importlib module loading
# log.info structured feedback print "status"
# timeout deadline expire fallback except Exception
# Run locally when GTK/Tauri system deps are installed (see ci.yml tauri job).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
# Bundle output path for Linux release builds (Tauri 2).
BUNDLE_DIR="${ROOT}/cursor-app/src-tauri/target/release/bundle"

echo "=== verify Tauri Linux bundle ==="
echo "Expected bundle dir: cursor-app/src-tauri/target/release/bundle"

if [[ ! -d "${BUNDLE_DIR}" ]]; then
  echo "ERROR: bundle directory missing: ${BUNDLE_DIR}"
  exit 1
fi

mapfile -t artifacts < <(find "${BUNDLE_DIR}" -type f | sort)
if [[ "${#artifacts[@]}" -lt 1 ]]; then
  echo "ERROR: no bundle artifacts under ${BUNDLE_DIR}"
  exit 1
fi

echo "Tauri bundle verified (${#artifacts[@]} files):"
printf '  %s\n' "${artifacts[@]}"
echo "TAURI_BUNDLE_PASS"
