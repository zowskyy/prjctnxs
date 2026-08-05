# Global Skill System — Five-Star Only Mandate

## Rule 1: Five-Star Only

All agent work on Project Nexus must be:

- **100% complete** — no placeholders, no skeleton-only deliverables
- **Immediately actionable** — builds, runs, and verifies in CI
- **Fully verified** — tests pass before the task is closed
- **No pending work** — no "push later", "TODO", or "executing" handoffs
- **Honest when blocked** — if a dependency (credentials, GPU hardware) is missing, ship the complete automation to resolve it and document the exact gap

## Rule 2: Completeness Checklist

Before closing any task, verify:

- [ ] All requested components implemented (not stubbed without disclosure)
- [ ] All tests passing (`cargo test`, `python3 -m unittest discover -s tests`)
- [ ] Documentation updated for user-facing changes
- [ ] Submodule changes committed; push script run when `GITHUB_TOKEN` is available
- [ ] Dependencies resolved in `Cargo.toml` / `package.json`
- [ ] ARC orchestrator gates pass where applicable

## Rule 3: Quality Bar

| Stars | Meaning | Allowed |
|-------|---------|---------|
| ⭐⭐⭐⭐⭐ | Complete, verified, production-ready | **Yes — required** |
| ⭐⭐⭐⭐☆ | Partial / missing pieces | **No** |
| ⭐⭐⭐☆☆ | Skeleton only | **No** |
| ⭐⭐☆☆☆ | Major gaps | **No** |
| ⭐☆☆☆☆ | Non-functional | **No** |

## Rule 4: Language Ecosystem

| Extension | Role |
|-----------|------|
| `.frontier` | Design spec / pseudo-code (human-readable, gates) |
| `.fr` | Validated source (parser + compiler input) |
| `.fbc` | Bytecode (VM input) |

Specs inform implementation; implementation validates specs. Both are versioned together.

## Rule 5: GPU & Native Toolchain

- **GPU:** Prefer real Vulkan when loader + device exist; fall back to software rasterizer in CI/headless.
- **Native compile:** Detect `llc`/`cc`/`clang`; emit IR always; link when toolchain is present; print install instructions when not.
