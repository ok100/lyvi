use crate::lyrics::Lyrics;
use ratatui_image::protocol::StatefulProtocol;
use std::time::Duration;

#[derive(Default)]
pub struct Track {
    pub artist: String,
    pub title: String,
    pub album: String,
    pub is_playing: bool,
    pub position: Duration,
    pub lyrics: Lyrics,
    pub album_art: Option<StatefulProtocol>,
}

impl Track {
    pub fn tick(&mut self, delta: Duration) {
        if self.is_playing {
            self.position += delta;
        }
    }
}

impl std::fmt::Debug for Track {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("Track")
            .field("artist", &self.artist)
            .field("title", &self.title)
            .field("album", &self.album)
            .field("is_playing", &self.is_playing)
            .field("position", &self.position)
            .field("lyrics", &self.lyrics)
            .field(
                "album_art",
                &self.album_art.as_ref().map(|_| "<StatefulProtocol>"),
            )
            .finish()
    }
}
