use std::future;

use crate::player::{Player, PlayerEvent};
use async_trait::async_trait;

pub struct MprisPlayer;

impl MprisPlayer {
    pub fn new() -> Self {
        Self {}
    }
}

#[async_trait]
impl Player for MprisPlayer {
    async fn next_event(&mut self) -> PlayerEvent {
        future::pending().await
    }
}
