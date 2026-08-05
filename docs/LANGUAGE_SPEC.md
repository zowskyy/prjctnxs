# Frontier Language Specification

## File Extensions

| Extension | Purpose |
|-----------|---------|
| `.frontier` | Design spec and pseudo-code (ARC gates, documentation) |
| `.fr` | Validated Frontier source (lexer/parser/compiler input) |
| `.fbc` | Compiled Frontier bytecode (VM executable) |

## Pipeline

```
.frontier  →  (human design, structural verification)
.fr        →  parse → resolve → compile → .fbc
.fbc       →  VM execute / JIT hot paths / native via LLVM IR
```

## Relationship

1. **`.frontier`** files describe intent: modules, APIs, and benchmarks. They are checked by the ARC orchestrator (marker gates) and guide Rust implementation.
2. **`.fr`** files are the canonical compile target for `frontier compile` and `frontier run`.
3. **`.fbc`** files are portable bytecode modules (magic `FBC\x01`) executed by the Frontier VM.

## CLI

```bash
frontier compile program.fr              # → program.fbc (default)
frontier compile program.fr --target wasm
frontier compile program.fr --target native
frontier run program.fbc
frontier run program.fr                  # compile + execute
frontier debug program.fr [--break N]
```

## Versioning

Spec (`.frontier`) and implementation (`.fr` / Rust runtime) are versioned in the same repository. Archived generations live under `archive/`; live canonical specs have no `v2`/`v3` suffix in tree root.
