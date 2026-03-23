mod app;
mod event;
mod handler;
mod lyrics;
mod player;
mod tasks;
mod track;
mod ui;

use crate::event::Events;
use app::App;
use color_eyre::Result;
use ratatui::DefaultTerminal;
use std::time::Duration;
use tokio_util::sync::CancellationToken;

const TICK_RATE: Duration = Duration::from_millis(16);

#[tokio::main]
async fn main() -> Result<()> {
    color_eyre::install()?;
    let mut terminal = ratatui::init();
    let result = run(&mut terminal).await;
    ratatui::restore();
    result
}

async fn run(terminal: &mut DefaultTerminal) -> Result<()> {
    let mut app = App::new();
    let mut events = Events::new(TICK_RATE);
    let mut fetch_token = CancellationToken::new();

    while app.is_running {
        terminal.draw(|frame| ui::render(frame, &app))?;
        if let Some(event) = events.next().await {
            handler::handle_event(&mut app, event, &events.sender, &mut fetch_token)?;
        }
    }

    Ok(())
}
