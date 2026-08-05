# MCPE Complexity Reduction Audit

**Generated:** 2026-08-05T14:48:15Z
**Model:** MCPE — power preserved, architecture simplified

## Summary

| Metric | Value |
|--------|-------|
| Live `.frontier` specs | 39 |
| Archived versioned specs | 13 |
| Verify modules (pre-unification) | 6 |

## Redundancies Identified

- verify_file_markers duplicated in 3 verify modules → unified in validator.py
- v2/v3 spec generations archived under archive/ (13 files)
- patches/backups/ duplicates live frontier/ai — candidate for removal

## Simplifications Applied

- UnifiedValidator for structural + metric gates
- FrontierBridge.execute() single Rust entry point
- Canonical live specs only (no v2/v3 in tree root)
- engine/ Rust workspace for runtime (nexus-runtime crate)

## Power Preservation (v2.5 Floors)

- **neural_fps_floor:** 1000
- **neural_accuracy_floor:** 0.99
- **render_fps_floor:** 240
- **compiler_speedup_floor:** 200
- **lm_latency_ceiling_ms:** 2.5

## Not Yet Implemented (Honest Gap)

- Native .frontier bytecode VM (WASM path only)
- Vulkan/DX12 GPU renderer
- 1024 Hz game loop with 1000+ entities (stub crate only)
- Real 16K path tracing
- Full neural training stack

## File Categories

### Live specs (canonical)

- `benchmark/spirits_within/benchmark.frontier`
- `benchmark/spirits_within/character.frontier`
- `benchmark/spirits_within/facial.frontier`
- `benchmark/spirits_within/final_fantasy_visualizer_ultra.frontier`
- `benchmark/spirits_within/lip_sync.frontier`
- `benchmark/spirits_within/materials.frontier`
- `benchmark/spirits_within/optimization.frontier`
- `benchmark/spirits_within/scene.frontier`
- `benchmark/spirits_within/volumetrics.frontier`
- `cursor/src/ai/chat.frontier`
- `cursor/src/ai/completion.frontier`
- `cursor/src/ai/context.frontier`
- `cursor/src/ai/engine.frontier`
- `cursor/src/ai/knowledge/hypercube.frontier`
- `cursor/src/app.frontier`
- `cursor/src/build/system.frontier`
- `cursor/src/editor/core.frontier`
- `cursor/src/explorer/explorer.frontier`
- `cursor/src/lsp/services.frontier`
- `cursor/src/optimization/performance.frontier`
- ... and 19 more
