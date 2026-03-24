use crate::cli::PlayerChoice;
use async_trait::async_trait;
use color_eyre::Result;
use image::DynamicImage;
use std::path::PathBuf;
use std::time::Duration;

pub mod mpd;

#[cfg(target_os = "macos")]
pub mod macos;

#[cfg(target_os = "linux")]
pub mod mpris;

pub struct PlayerMetadata {
    pub artist: String,
    pub title: String,
    pub album: String,
    pub album_art: Option<DynamicImage>,
    pub file: Option<PathBuf>,
    pub is_playing: bool,
    pub position: Duration,
}

pub enum PlayerEvent {
    StateChanged(PlayerMetadata),
    Stopped,
    Disconnected,
}

#[async_trait]
pub trait Player: Send {
    async fn next_event(&mut self) -> PlayerEvent;
}

pub fn resolve(choice: PlayerChoice) -> Result<Box<dyn Player>> {
    match choice {
        PlayerChoice::Mpd => Ok(Box::new(mpd::MpdPlayer::new())),

        #[cfg(target_os = "macos")]
        PlayerChoice::Macos => Ok(Box::new(macos::MacOsPlayer::new())),

        #[cfg(target_os = "linux")]
        PlayerChoice::Mpris => Ok(Box::new(mpris::MprisPlayer::new())),
    }
}
