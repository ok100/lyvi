use std::future;

use crate::player::{Player, PlayerEvent};
use async_trait::async_trait;

pub struct MpdPlayer;

impl MpdPlayer {
    pub fn new() -> Self {
        Self {}
    }
}

#[async_trait]
impl Player for MpdPlayer {
    async fn next_event(&mut self) -> PlayerEvent {
        future::pending().await
    }
}
