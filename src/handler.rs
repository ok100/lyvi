use crate::TICK_RATE;
use crate::app::App;
use crate::event::Event;
use crate::tasks::TaskManager;
use color_eyre::Result;
use crossterm::event::{KeyCode, KeyEventKind};

pub fn handle_event(app: &mut App, event: Event, tasks: &mut TaskManager) -> Result<()> {
    match event {
        Event::Tick => app.tick(TICK_RATE),

        Event::Key(key) => {
            if key.kind == KeyEventKind::Press {
                match key.code {
                    KeyCode::Char('q') | KeyCode::Esc => app.quit(),
                    _ => {}
                }
            }
        }

        Event::PlayerStateChanged(metadata) => {
            if app.is_new_track(&metadata) {
                tasks.cancel();
                app.set_track(metadata);
                tasks.fetch_lyrics();
                tasks.fetch_album_art();
            } else {
                app.set_playing(metadata.is_playing);
                app.sync_position(metadata.position);
            }
        }

        Event::PlaybackStopped | Event::PlayerDisconnected => {
            tasks.cancel();
            app.clear_track();
        }

        Event::LyricsReady(lyrics) => app.set_lyrics(lyrics),

        Event::AlbumArtReady(protocol) => app.set_album_art(protocol),
    }

    Ok(())
}
