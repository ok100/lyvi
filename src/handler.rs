use crate::TICK_RATE;
use crate::app::App;
use crate::event::Event;
use crate::tasks;
use color_eyre::Result;
use crossterm::event::{KeyCode, KeyEventKind};
use tokio::sync::mpsc;
use tokio_util::sync::CancellationToken;

pub fn handle_event(
    app: &mut App,
    event: Event,
    sender: &mpsc::UnboundedSender<Event>,
    fetch_token: &mut CancellationToken,
) -> Result<()> {
    let mut cancel_fetch_tasks = || {
        fetch_token.cancel();
        *fetch_token = CancellationToken::new();
    };

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
                cancel_fetch_tasks();
                app.set_track(metadata);
                tasks::fetch_lyrics(sender.clone(), fetch_token.clone());
                tasks::fetch_album_art(sender.clone(), fetch_token.clone());
            } else {
                app.set_playing(metadata.is_playing);
                app.sync_position(metadata.position);
            }
        }

        Event::PlaybackStopped | Event::PlayerDisconnected => {
            cancel_fetch_tasks();
            app.clear_track();
        }

        Event::LyricsReady(lyrics) => app.set_lyrics(lyrics),

        Event::AlbumArtReady(protocol) => app.set_album_art(protocol),
    }

    Ok(())
}
