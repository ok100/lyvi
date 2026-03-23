use crate::lyrics::Lyrics;
use crate::player::{Player, PlayerEvent, PlayerMetadata};
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
    PlayerDisconnected,
    LyricsReady(Lyrics),
    AlbumArtReady(StatefulProtocol),
}

impl From<PlayerEvent> for Event {
    fn from(player_event: PlayerEvent) -> Self {
        match player_event {
            PlayerEvent::StateChanged(metadata) => Event::PlayerStateChanged(metadata),
            PlayerEvent::Stopped => Event::PlaybackStopped,
            PlayerEvent::Disconnected => Event::PlayerDisconnected,
        }
    }
}

pub struct Events {
    pub sender: mpsc::UnboundedSender<Event>,
    receiver: mpsc::UnboundedReceiver<Event>,
}

impl Events {
    pub fn new(tick_rate: Duration, player: Box<dyn Player>) -> Self {
        let (sender, receiver) = mpsc::unbounded_channel();

        Self::spawn_key_listener(sender.clone(), tick_rate);
        Self::spawn_tick_timer(sender.clone(), tick_rate);
        Self::spawn_player_listener(sender.clone(), player);

        Self { sender, receiver }
    }

    fn spawn_key_listener(sender: mpsc::UnboundedSender<Event>, tick_rate: Duration) {
        tokio::task::spawn_blocking(move || {
            loop {
                if event::poll(tick_rate).unwrap_or(false)
                    && let Ok(CrosstermEvent::Key(key)) = event::read()
                    && sender.send(Event::Key(key)).is_err()
                {
                    break;
                }

                if sender.is_closed() {
                    break;
                }
            }
        });
    }

    fn spawn_tick_timer(sender: mpsc::UnboundedSender<Event>, tick_rate: Duration) {
        tokio::spawn(async move {
            let mut ticker = time::interval(tick_rate);
            loop {
                ticker.tick().await;
                if sender.send(Event::Tick).is_err() {
                    break;
                }
            }
        });
    }

    fn spawn_player_listener(sender: mpsc::UnboundedSender<Event>, mut player: Box<dyn Player>) {
        tokio::spawn(async move {
            loop {
                let event = player.next_event().await;

                if matches!(event, PlayerEvent::Disconnected) {
                    break;
                }

                if sender.send(event.into()).is_err() {
                    break;
                }
            }
        });
    }

    pub async fn next(&mut self) -> Option<Event> {
        self.receiver.recv().await
    }
}
