#!/usr/bin/env bash
# Push frontier-syntax submodule after full verification.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SUBMODULE="${ROOT}/external/frontier-syntax"

echo "🚀 Five-Star Submodule Push — frontier-syntax"
echo "   Root: ${ROOT}"

if [[ ! -e "${SUBMODULE}/.git" ]]; then
  echo "❌ Submodule not initialized. Run: git submodule update --init --recursive"
  exit 1
fi

cd "${SUBMODULE}"

echo "📦 Running tests..."
cargo test --lib
cargo test --test runtime_suite

echo "🔨 Release build..."
cargo build --release --bin frontier

if [[ -z "${GITHUB_TOKEN:-}" ]]; then
  echo "⚠️  GITHUB_TOKEN not set — skipping remote push."
  echo "   Export GITHUB_TOKEN with repo write access, then re-run:"
  echo "   GITHUB_TOKEN=... ${ROOT}/scripts/push_submodule.sh"
  exit 0
fi

BRANCH="${FRONTIER_SYNTAX_BRANCH:-main}"
REMOTE_URL="https://${GITHUB_TOKEN}@github.com/zowskyy/frontier-syntax.git"

git remote set-url origin "${REMOTE_URL}"
git push origin "HEAD:${BRANCH}"
git remote set-url origin "https://github.com/zowskyy/frontier-syntax.git"

echo "✅ Submodule pushed to origin/${BRANCH}"

cd "${ROOT}"
git add external/frontier-syntax
if git diff --cached --quiet; then
  echo "✅ Parent repo already pins current submodule SHA"
else
  git commit -m "chore: update frontier-syntax submodule pointer"
  git push origin "$(git branch --show-current)"
  echo "✅ Parent repo updated with new submodule SHA"
fi
