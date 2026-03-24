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

        Event::PlayerStateChanged(mut metadata) => {
            if app.is_new_track(&metadata) {
                tasks.cancel();
                let art = metadata.album_art.take();
                app.set_track(metadata);
                tasks.fetch_lyrics();
                if let Some(album_art) = art {
                    tasks.process_album_art(album_art);
                } else {
                    tasks.fetch_album_art();
                }
            } else {
                app.set_playing(metadata.is_playing);
                app.sync_position(metadata.position);
                if app.needs_album_art()
                    && let Some(album_art) = metadata.album_art.take()
                {
                    tasks.process_album_art(album_art);
                }
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
