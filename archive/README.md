# Archived Versioned Specs

Versioned `.frontier` files (`*_v2.frontier`, `*_v3.frontier`) were moved here during the
**Real Implementation Bridge** collapse. Active development uses:

- **Implementation:** `external/frontier-syntax` (Rust submodule)
- **Bridge:** `build/rust_bridge.py`
- **Vertical slice:** `build/vertical_slice.py`
- **Live specs:** non-versioned files under `frontier/`, `cursor/`, `src/`

Run `python3 build/arc_orchestrator.py --verify-real` for behavioral verification.
