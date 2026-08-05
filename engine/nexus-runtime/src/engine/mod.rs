//! Game loop — fixed timestep update with frame pacing metrics.

use std::time::{Duration, Instant};

use crate::ecs::{SystemSet, World};

pub const TARGET_HZ: f64 = 1024.0;
const FIXED_DT: f32 = 1.0 / TARGET_HZ as f32;

pub struct GameLoop {
    pub world: World,
    pub running: bool,
    pub tick_count: u64,
    pub last_hz: f64,
}

impl Default for GameLoop {
    fn default() -> Self {
        Self::new()
    }
}

impl GameLoop {
    pub fn new() -> Self {
        Self {
            world: World::new(),
            running: true,
            tick_count: 0,
            last_hz: 0.0,
        }
    }

    pub fn with_entities(count: usize) -> Self {
        let mut loop_ = Self::new();
        for id in loop_.world.spawn_batch(count) {
            if let Some(v) = loop_.world.velocity_mut(id) {
                v.dx = 1.0;
                v.dy = 0.5;
            }
        }
        loop_
    }

    pub fn update(&mut self) {
        SystemSet::physics(&mut self.world, FIXED_DT);
        self.tick_count += 1;
    }

    /// Run `ticks` updates and return measured Hz.
    pub fn bench_ticks(&mut self, ticks: u64) -> f64 {
        let start = Instant::now();
        for _ in 0..ticks {
            self.update();
        }
        let elapsed = start.elapsed().as_secs_f64();
        self.last_hz = ticks as f64 / elapsed.max(1e-9);
        self.last_hz
    }

    /// Run for `duration` and return average Hz.
    pub fn run_for(&mut self, duration: Duration) -> f64 {
        let start = Instant::now();
        let mut count = 0u64;
        while start.elapsed() < duration {
            self.update();
            count += 1;
        }
        let elapsed = start.elapsed().as_secs_f64();
        self.last_hz = count as f64 / elapsed.max(1e-9);
        self.last_hz
    }

    pub fn meets_target(&self, min_hz: f64, min_entities: usize) -> bool {
        self.world.entity_count() >= min_entities && self.last_hz >= min_hz
    }
}
