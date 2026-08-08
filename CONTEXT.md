# CONTEXT.md — SnapForge Android Game Studio

**Last updated:** 2026-08-08T02:58:00Z  
**Session:** Cloud Agent roadmap audit + GA remediation  
**Status:** Active

## Project

SnapForge Android Game Studio — extending Nexumis SnapForge (block-based visual scripting for Playstudio, Windows-only) into a GA-ready Android game development studio with Vulkan rendering, AAB export, and Google Play Games Services v2.

## Current State

- **Original docx:** `C:\Users\thewi\Downloads\SnapForge_Android_Game_Studio_Roadmap (1).docx` — not accessible in cloud workspace; audit reconstructed from public sources.
- **Deliverables this session:**
  - `docs/SnapForge_Android_Game_Studio_Roadmap.md` — GA-passing roadmap
  - `tools/snapforge_roadmap_tracker.py` — checkpoint tracker (`~/.crawler/state.json`)
  - `tests/test_snapforge_roadmap_tracker.py` — verification-first tests
- **Architecture decision:** Branch B (cross-platform editor + NDK Vulkan runtime)
- **Branch:** `cursor/snapforge-android-roadmap-af05`

## Key Metrics (Targets)

| Phase | KPI Target |
|:------|:-----------|
| P0 Foundation | 100% block schema coverage |
| P1 Android Shell | ≤2.5s cold start, ≥60 FPS editor |
| P2 Compiler | ≥99.5% compile success, ≤800ms p95 |
| P3 Renderer | ≥4000 draw calls, ≤2ms frame jitter |
| P4 Play Store | ≥99% GPGS sign-in, 0 policy blocks |
| P5 GA | ≥99.5% crash-free, ≥1000 concurrent publishers |

## Next Actions

1. Review PR and merge roadmap into main
2. Begin P0: formalize `gates/snapforge_blocks.json` from Windows SnapForge schema
3. Spike P1: Android target for Tauri shell

## References

- Public SnapForge: https://nexumis.itch.io/snapforge
- Vulkan on Android (2026): https://developer.android.com/games/develop/vulkan/overview
- GPGS release notes: https://developer.android.com/games/docs/release-notes
