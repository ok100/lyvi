use crate::lyrics::Lyrics;
use crate::player::PlayerMetadata;
use crate::track::Track;
use ratatui_image::protocol::StatefulProtocol;
use std::time::Duration;

pub struct App {
    pub is_running: bool,
    pub track: Option<Track>,
}

impl Default for App {
    fn default() -> Self {
        Self {
            is_running: true,
            track: None,
        }
    }
}

impl App {
    pub fn new() -> Self {
        Self::default()
    }

    pub fn quit(&mut self) {
        self.is_running = false;
    }

    pub fn set_track(&mut self, metadata: PlayerMetadata) {
        self.track = Some(Track {
            artist: metadata.artist,
            title: metadata.title,
            album: metadata.album,
            is_playing: metadata.is_playing,
            position: metadata.position,
            ..Track::default()
        });
    }

    pub fn clear_track(&mut self) {
        self.track = None;
    }

    pub fn is_new_track(&self, metadata: &PlayerMetadata) -> bool {
        self.track
            .as_ref()
            .map(|track| {
                track.artist != metadata.artist
                    || track.title != metadata.title
                    || track.album != metadata.album
            })
            .unwrap_or(true)
    }

    pub fn set_playing(&mut self, is_playing: bool) {
        if let Some(track) = self.track.as_mut() {
            track.is_playing = is_playing;
        }
    }

    pub fn sync_position(&mut self, position: Duration) {
        if let Some(track) = self.track.as_mut() {
            track.position = position;
        }
    }

    pub fn tick(&mut self, delta: Duration) {
        if let Some(track) = self.track.as_mut() {
            track.tick(delta)
        }
    }

    pub fn set_lyrics(&mut self, lyrics: Lyrics) {
        if let Some(track) = self.track.as_mut() {
            track.lyrics = lyrics;
        }
    }

    pub fn set_album_art(&mut self, protocol: StatefulProtocol) {
        if let Some(track) = self.track.as_mut() {
            track.album_art = Some(protocol);
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::player::PlayerMetadata;
    use std::time::Duration;

    fn make_metadata(artist: &str, title: &str, album: &str) -> PlayerMetadata {
        PlayerMetadata {
            artist: artist.to_string(),
            title: title.to_string(),
            album: album.to_string(),
            file: None,
            is_playing: true,
            position: Duration::ZERO,
        }
    }

    #[test]
    fn new_track_when_no_track_playing() {
        let app = App::new();
        let metadata = make_metadata("Artist", "Title", "Album");
        assert!(app.is_new_track(&metadata));
    }

    #[test]
    fn new_track_when_metadata_differs() {
        let mut app = App::new();
        app.set_track(make_metadata("Artist A", "Title", "Album"));
        assert!(app.is_new_track(&make_metadata("Artist B", "Title", "Album")));
    }

    #[test]
    fn not_new_track_when_same_metadata() {
        let mut app = App::new();
        app.set_track(make_metadata("Artist", "Title", "Album"));
        assert!(!app.is_new_track(&make_metadata("Artist", "Title", "Album")));
    }
}
