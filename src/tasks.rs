use crate::event::Event;
use image::DynamicImage;
use ratatui_image::picker::Picker;
use tokio::sync::mpsc::UnboundedSender;
use tokio_util::sync::CancellationToken;

pub struct TaskManager {
    sender: UnboundedSender<Event>,
    token: CancellationToken,
    picker: Picker,
}

impl TaskManager {
    pub fn new(sender: UnboundedSender<Event>, picker: Picker) -> Self {
        Self {
            sender,
            token: CancellationToken::new(),
            picker,
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

    pub fn process_album_art(&self, image: DynamicImage) {
        let sender = self.sender.clone();
        let token = self.token.clone();
        let picker = self.picker.clone();
        tokio::spawn(async move {
            tokio::select! {
                _ = token.cancelled() => {}
                result = tokio::task::spawn_blocking(move || {
                    picker.new_resize_protocol(image)
                }) => {
                    if let Ok(protocol) = result {
                        let _ = sender.send(Event::AlbumArtReady(protocol));
                    }
                }
            }
        });
    }
}
