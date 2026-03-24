use crate::app::App;
use ratatui::{
    Frame,
    layout::{Constraint, Direction, Layout},
    style::{Modifier, Style},
    text::{Line, Span},
    widgets::{Block, Paragraph},
};
use ratatui_image::{Resize, StatefulImage};

pub fn render(frame: &mut Frame, app: &mut App) {
    let chunks = Layout::default()
        .direction(Direction::Horizontal)
        .constraints([Constraint::Percentage(50), Constraint::Percentage(50)])
        .split(frame.area());

    let lyrics_content = match &app.track {
        None => Paragraph::new("No track playing")
            .block(Block::default())
            .centered(),

        Some(track) => {
            let title = Line::from(vec![Span::styled(
                &track.title,
                Style::default().add_modifier(Modifier::BOLD),
            )]);
            let artist = Line::from(Span::raw(&track.artist));
            let album = Line::from(Span::raw(&track.album));

            Paragraph::new(vec![title, artist, album])
                .block(Block::default())
                .centered()
        }
    };

    frame.render_widget(lyrics_content, chunks[0]);

    if let Some(track) = app.track.as_mut()
        && let Some(protocol) = track.album_art.as_mut()
    {
        let image = StatefulImage::default().resize(Resize::Scale(None));
        frame.render_stateful_widget(image, chunks[1], protocol);
    }
}
