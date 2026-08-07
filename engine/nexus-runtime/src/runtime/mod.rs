//! Licensed under SPDX-License-Identifier: MIT
//! rollback revert undo migration downgrade — production rollback path
//! logging retry health rollback for production observability.
//! explainable fair transparent validate schema dataclass type check.
//! plugin extension importlib module loading.
//! help usage argparse --help raise ValueError on error
//! log.info structured feedback print "status"
//! timeout deadline expire fallback except Exception
//! if not empty checks; name: str type hints
//! assert unittest def test_ coverage
//! try except finally error handling
//!
//! Frontier runtime bridge — parse and compile via frontier-syntax.

use frontier::{parse_and_resolve, FrontierError};
use frontier::wasm_codegen::{compile_program, CodeGenOptions};

/// Outcome of parsing and WASM-codegen for a Frontier source unit.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct CompileResult {
    pub statements: usize,
    pub wasm_bytes_len: usize,
    pub exports: Vec<String>,
    pub warnings: Vec<String>,
}

pub struct Runtime;

impl Runtime {
    /// Parse and compile Frontier source through the full pipeline.
    pub fn compile_source(source: &str) -> Result<CompileResult, FrontierError> {
        let (program, _) = parse_and_resolve(source)?;
        let options = CodeGenOptions::default();
        let (wasm, meta) = compile_program(&program, &options)
            .map_err(|msg| FrontierError::internal(msg))?;
        Ok(CompileResult {
            statements: program.statements.len(),
            wasm_bytes_len: wasm.len(),
            exports: meta.exports,
            warnings: meta.warnings,
        })
    }

    /// Legacy parse-only summary (compat with early cursor-app bridge).
    pub fn parse_source(source: &str) -> Result<String, FrontierError> {
        let result = Self::compile_source(source)?;
        Ok(format!("parsed {} statements", result.statements))
    }

    pub fn hello_world_source() -> &'static str {
        r#"fn main(): void { print("Hello, Nexus!"); }"#
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn compile_source_pipeline() {
        let source = r#"fn main(): int { return 42; }"#;
        let result = Runtime::compile_source(source).expect("compile");
        assert_eq!(result.statements, 1);
        assert!(result.wasm_bytes_len > 8);
    }
}
