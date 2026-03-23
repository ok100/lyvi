use super::{Player, PlayerEvent, PlayerMetadata};
use async_trait::async_trait;
use media_remote::{ListenerToken, NowPlayingInfo, NowPlayingPerl, Subscription};
use std::time::Duration;
use tokio::sync::mpsc;

pub struct MacOsPlayer {
    receiver: mpsc::UnboundedReceiver<PlayerEvent>,
    _now_playing: NowPlayingPerl,
    _token: ListenerToken,
}

impl MacOsPlayer {
    pub fn new() -> Self {
        let (sender, receiver) = mpsc::unbounded_channel();
        let now_playing = NowPlayingPerl::new();

        let token = now_playing.subscribe(move |guard| {
            let event = match guard.as_ref() {
                Some(info) => PlayerEvent::StateChanged(Self::to_metadata(info)),
                None => PlayerEvent::Stopped,
            };
            let _ = sender.send(event);
        });

        Self {
            receiver,
            _now_playing: now_playing,
            _token: token,
        }
    }

    fn to_metadata(info: &NowPlayingInfo) -> PlayerMetadata {
        PlayerMetadata {
            artist: info.artist.clone().unwrap_or_default(),
            title: info.title.clone().unwrap_or_default(),
            album: info.album.clone().unwrap_or_default(),
            file: None,
            is_playing: info.is_playing.unwrap_or(false),
            position: Duration::from_secs_f64(info.elapsed_time.unwrap_or(0.0)),
        }
    }
}

#[async_trait]
impl Player for MacOsPlayer {
    async fn next_event(&mut self) -> PlayerEvent {
        self.receiver
            .recv()
            .await
            .unwrap_or(PlayerEvent::Disconnected)
    }
}

impl Drop for MacOsPlayer {
    fn drop(&mut self) {
        self._now_playing.unsubscribe(self._token.clone());
    }
}
