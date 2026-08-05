//! Project Nexus runtime — ECS, game loop, Frontier scripting bridge.

pub mod ecs;
pub mod engine;
pub mod runtime;

pub use ecs::{Entity, Transform, Velocity, World};
pub use engine::{GameLoop, TARGET_HZ};
pub use runtime::Runtime;

/// Unified engine facade for integration tests and benchmarks.
pub struct NexusEngine {
    pub loop_: GameLoop,
}

impl Default for NexusEngine {
    fn default() -> Self {
        Self::new()
    }
}

impl NexusEngine {
    pub fn new() -> Self {
        Self {
            loop_: GameLoop::with_entities(1000),
        }
    }

    pub fn bench_ecs(&mut self, ticks: u64) -> f64 {
        self.loop_.bench_ticks(ticks)
    }

    pub fn meets_arc_gate(&self) -> bool {
        self.loop_.meets_target(TARGET_HZ, 1000)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::time::Duration;

    #[test]
    fn ecs_spawns_entities() {
        let mut world = World::new();
        let ids = world.spawn_batch(1000);
        assert_eq!(ids.len(), 1000);
        assert_eq!(world.entity_count(), 1000);
    }

    #[test]
    fn game_loop_exceeds_1024_hz() {
        let mut loop_ = GameLoop::with_entities(1000);
        let hz = loop_.bench_ticks(50_000);
        assert!(
            hz >= TARGET_HZ,
            "expected >= {TARGET_HZ} Hz, got {hz:.0}"
        );
    }

    #[test]
    fn frontier_parse_bridge() {
        let summary = Runtime::parse_source("fn add(a: i32, b: i32) -> i32 { return a + b; }");
        assert!(summary.is_ok());
    }

    #[test]
    fn nexus_engine_arc_gate() {
        let mut engine = NexusEngine::new();
        engine.bench_ecs(10_000);
        assert!(engine.meets_arc_gate());
    }

    #[test]
    fn sustained_tick_rate() {
        let mut loop_ = GameLoop::with_entities(1500);
        let hz = loop_.run_for(Duration::from_millis(100));
        assert!(hz >= TARGET_HZ, "sustained {hz:.0} Hz < {TARGET_HZ}");
    }
}
