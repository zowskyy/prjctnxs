//! Frontier runtime bridge — parse and compile via frontier-syntax.

use frontier::{parse_and_resolve, FrontierError};

pub struct Runtime;

impl Runtime {
    pub fn parse_source(source: &str) -> Result<String, FrontierError> {
        let (program, _) = parse_and_resolve(source)?;
        Ok(format!("parsed {} statements", program.statements.len()))
    }

    pub fn hello_world_source() -> &'static str {
        r#"fn main(): void { print("Hello, Nexus!"); }"#
    }
}
