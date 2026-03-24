mod app;
mod cli;
mod event;
mod handler;
mod lyrics;
mod player;
mod tasks;
mod track;
mod ui;

use crate::cli::Args;
use crate::event::Events;
use crate::player::Player;
use crate::tasks::TaskManager;
use app::App;
use clap::Parser;
use color_eyre::Result;
use ratatui::DefaultTerminal;
use ratatui_image::picker::Picker;
use std::time::Duration;

const TICK_RATE: Duration = Duration::from_millis(16);

#[tokio::main]
async fn main() -> Result<()> {
    color_eyre::install()?;
    let args = Args::parse();
    let player = player::resolve(args.player)?;
    let picker = Picker::from_query_stdio().unwrap_or_else(|_| Picker::halfblocks());
    let mut terminal = ratatui::init();
    let result = run(&mut terminal, player, picker).await;
    ratatui::restore();
    result
}

async fn run(
    terminal: &mut DefaultTerminal,
    player: Box<dyn Player>,
    picker: Picker,
) -> Result<()> {
    let mut app = App::new();
    let mut events = Events::new(TICK_RATE, player);
    let mut tasks = TaskManager::new(events.sender.clone(), picker);

    while app.is_running {
        terminal.draw(|frame| ui::render(frame, &mut app))?;
        if let Some(event) = events.next().await {
            handler::handle_event(&mut app, event, &mut tasks)?;
        }
    }

    Ok(())
}
