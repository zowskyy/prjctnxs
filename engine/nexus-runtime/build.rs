//! WASM / Frontier spec hooks for the Nexus runtime build.
fn main() {
    let frontier_root = std::path::Path::new("external/frontier-syntax");
    if frontier_root.join("Cargo.toml").exists() {
        println!("cargo:rerun-if-changed=../../external/frontier-syntax/Cargo.toml");
    }
    for dir in ["frontier", "benchmark"] {
        let path = format!("../../{dir}");
        if std::path::Path::new(&path).exists() {
            println!("cargo:rerun-if-changed={path}");
        }
    }
    println!("cargo:rustc-env=NEXUS_BUILD_TS={}", chrono_like_ts());
}

fn chrono_like_ts() -> String {
    use std::time::{SystemTime, UNIX_EPOCH};
    let secs = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .map(|d| d.as_secs())
        .unwrap_or(0);
    format!("{secs}")
}
