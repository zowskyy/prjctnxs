# MCPE Deployment — Project Nexus v3.0

## Overview

Project Nexus v3.0 ships as a **Cargo workspace** with three primary artifacts:

| Component | Path | Role |
|-----------|------|------|
| Frontier compiler | `external/frontier-syntax` | Parse, resolve, WASM compile |
| Game runtime | `engine/nexus-runtime` | ECS, 1024 Hz game loop |
| IDE shell | `cursor-app` | Tauri 2 + CodeMirror editor |

## Bootstrap

```bash
git clone --recursive https://github.com/zowskyy/prjctnxs.git
cd prjctnxs
npm run bootstrap          # submodule + frontend + Rust workspace
```

## Build

```bash
# Full workspace (frontend dist required for Tauri)
npm run build

# Runtime only
cargo build --release -p nexus-runtime

# IDE desktop app
cd cursor-app && npm run tauri:build
```

## Verify

```bash
python3 build/arc_orchestrator.py --verify-all
python3 build/integration_verify.py
cargo test -p nexus-runtime --release
python3 -m unittest discover -s tests -v
```

## MCPE Model

- **Power preserved:** v2.5 metric floors enforced in `build/validator.py`
- **Complexity reduced:** unified validator, canonical specs, `FrontierBridge.execute()`
- **Honest gaps:** GPU renderer, native `.frontier` VM, full neural training — scaffolded in specs; measured gates where Rust exists

## CI

GitHub Actions workflow `.github/workflows/ci.yml`:

1. **rust** — workspace build, nexus-runtime tests, ECS benchmark
2. **python** — 43+ unit tests, `--verify-real`
3. **frontend** — Vite build
4. **tauri** — Linux desktop bundle

## Publish (future)

```bash
cargo install --path engine/nexus-runtime --bin nexus-bench
# frontier publish --package engine  (MCPE registry — not yet wired)
```
