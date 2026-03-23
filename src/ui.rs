use crate::app::App;
use ratatui::{
    Frame,
    layout::{Constraint, Direction, Layout},
    widgets::{Block, Paragraph},
};

pub fn render(frame: &mut Frame, app: &App) {
    let chunks = Layout::default()
        .direction(Direction::Horizontal)
        .constraints([Constraint::Percentage(60), Constraint::Percentage(40)])
        .split(frame.area());

    let lyrics_content = Paragraph::new(app.is_running.to_string())
        .block(Block::default())
        .centered();
    frame.render_widget(lyrics_content, chunks[0]);

    let art_block = Block::default();
    frame.render_widget(art_block, chunks[1]);
}
