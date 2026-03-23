use std::path::PathBuf;
use std::time::Duration;

pub struct PlayerMetadata {
    pub artist: String,
    pub title: String,
    pub album: String,
    pub file: Option<PathBuf>,
    pub is_playing: bool,
    pub position: Duration,
}
