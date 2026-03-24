use crate::event::Event;
use tokio::sync::mpsc::UnboundedSender;
use tokio_util::sync::CancellationToken;

pub struct TaskManager {
    sender: UnboundedSender<Event>,
    token: CancellationToken,
}

impl TaskManager {
    pub fn new(sender: UnboundedSender<Event>) -> Self {
        Self {
            sender,
            token: CancellationToken::new(),
        }
    }

    pub fn cancel(&mut self) {
        self.token.cancel();
        self.token = CancellationToken::new()
    }

    pub fn fetch_lyrics(&self) {
        let _sender = self.sender.clone();
        let token = self.token.clone();
        tokio::spawn(async move {
            tokio::select! {
                _ = token.cancelled() => {}
                // TODO: fetch lyrics
            }
        });
    }

    pub fn fetch_album_art(&self) {
        let _sender = self.sender.clone();
        let token = self.token.clone();
        tokio::spawn(async move {
            tokio::select! {
                _ = token.cancelled() => {}
                // TODO: fetch album art
            }
        });
    }
}
