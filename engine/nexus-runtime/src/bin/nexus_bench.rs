//! CLI benchmark for ECS / game loop tick rate.

use nexus_runtime::{GameLoop, NexusEngine, TARGET_HZ};

fn main() {
    let ticks: u64 = std::env::args()
        .nth(1)
        .and_then(|s| s.parse().ok())
        .unwrap_or(100_000);

    let mut engine = NexusEngine::new();
    let hz = engine.bench_ecs(ticks);
    let entities = engine.loop_.world.entity_count();
    let gate = if engine.meets_arc_gate() { "PASS" } else { "FAIL" };

    println!("Nexus ECS Benchmark");
    println!("  entities: {entities}");
    println!("  ticks:    {ticks}");
    println!("  rate:     {hz:.0} Hz (target {TARGET_HZ:.0} Hz)");
    println!("  ARC gate: {gate}");

    let mut loop_ = GameLoop::with_entities(1000);
    let _ = loop_.bench_ticks(10_000);
    if !loop_.meets_target(TARGET_HZ, 1000) {
        std::process::exit(1);
    }
}
