use crate::lyrics::Lyrics;
use crate::player::PlayerMetadata;
use crossterm::event::{self, Event as CrosstermEvent, KeyEvent};
use ratatui_image::protocol::StatefulProtocol;
use std::time::Duration;
use tokio::sync::mpsc;
use tokio::time;

pub enum Event {
    Tick,
    Key(KeyEvent),
    PlayerStateChanged(PlayerMetadata),
    PlaybackStopped,
    LyricsReady(Lyrics),
    AlbumArtReady(StatefulProtocol),
}

pub struct Events {
    pub sender: mpsc::UnboundedSender<Event>,
    receiver: mpsc::UnboundedReceiver<Event>,
}

impl Events {
    pub fn new(tick_rate: Duration) -> Self {
        let (sender, receiver) = mpsc::unbounded_channel();

        let key_sender = sender.clone();
        tokio::task::spawn_blocking(move || {
            loop {
                if event::poll(tick_rate).unwrap_or(false)
                    && let Ok(CrosstermEvent::Key(key)) = event::read()
                    && key_sender.send(Event::Key(key)).is_err()
                {
                    break;
                }

                if key_sender.is_closed() {
                    break;
                }
            }
        });

        let tick_sender = sender.clone();
        tokio::spawn(async move {
            let mut ticker = time::interval(tick_rate);
            loop {
                ticker.tick().await;
                if tick_sender.send(Event::Tick).is_err() {
                    break;
                }
            }
        });

        // TODO: player task

        Self { sender, receiver }
    }

    pub async fn next(&mut self) -> Option<Event> {
        self.receiver.recv().await
    }
}
