use crate::event::Event;
use tokio::sync::mpsc::UnboundedSender;
use tokio_util::sync::CancellationToken;

pub fn fetch_lyrics(_sender: UnboundedSender<Event>, token: CancellationToken) {
    tokio::spawn(async move {
        tokio::select! {
            _ = token.cancelled() => {}
            // TODO: fetch lyrics
        }
    });
}

pub fn fetch_album_art(_sender: UnboundedSender<Event>, token: CancellationToken) {
    tokio::spawn(async move {
        tokio::select! {
            _ = token.cancelled() => {}
            // TODO: fetch album art
        }
    });
}
