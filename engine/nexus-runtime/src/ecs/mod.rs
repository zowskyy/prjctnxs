//! Entity Component System — stores entities and component data in SoA layout.

use std::any::{Any, TypeId};
use std::collections::HashMap;

pub type Entity = u32;

#[derive(Debug, Clone, Copy, Default)]
pub struct Transform {
    pub x: f32,
    pub y: f32,
    pub z: f32,
}

#[derive(Debug, Clone, Copy, Default)]
pub struct Velocity {
    pub dx: f32,
    pub dy: f32,
    pub dz: f32,
}

pub struct World {
    next_entity: Entity,
    transforms: HashMap<Entity, Transform>,
    velocities: HashMap<Entity, Velocity>,
    custom: HashMap<TypeId, Box<dyn Any + Send + Sync>>,
}

impl Default for World {
    fn default() -> Self {
        Self::new()
    }
}

impl World {
    pub fn new() -> Self {
        Self {
            next_entity: 1,
            transforms: HashMap::new(),
            velocities: HashMap::new(),
            custom: HashMap::new(),
        }
    }

    pub fn spawn(&mut self) -> Entity {
        let id = self.next_entity;
        self.next_entity += 1;
        self.transforms.insert(id, Transform::default());
        self.velocities.insert(id, Velocity::default());
        id
    }

    pub fn spawn_batch(&mut self, count: usize) -> Vec<Entity> {
        (0..count).map(|_| self.spawn()).collect()
    }

    pub fn entity_count(&self) -> usize {
        self.transforms.len()
    }

    pub fn transform_mut(&mut self, entity: Entity) -> Option<&mut Transform> {
        self.transforms.get_mut(&entity)
    }

    pub fn velocity_mut(&mut self, entity: Entity) -> Option<&mut Velocity> {
        self.velocities.get_mut(&entity)
    }

    pub fn update_physics(&mut self, dt: f32) {
        for (id, vel) in &self.velocities {
            if let Some(tr) = self.transforms.get_mut(id) {
                tr.x += vel.dx * dt;
                tr.y += vel.dy * dt;
                tr.z += vel.dz * dt;
            }
        }
    }
}

pub struct SystemSet;

impl SystemSet {
    pub fn physics(world: &mut World, dt: f32) {
        world.update_physics(dt);
    }
}
