use clap::{Parser, ValueEnum};

#[derive(Parser, Debug)]
#[command(version)]
pub struct Args {
    #[arg(long, value_enum)]
    #[cfg_attr(target_os = "macos", arg(default_value = "macos"))]
    #[cfg_attr(target_os = "linux", arg(default_value = "mpris"))]
    #[cfg_attr(
        not(any(target_os = "macos", target_os = "linux")),
        arg(default_value = "mpd")
    )]
    pub player: PlayerChoice,
}

#[derive(ValueEnum, Clone, Debug)]
pub enum PlayerChoice {
    Mpd,

    #[cfg(target_os = "macos")]
    Macos,

    #[cfg(target_os = "linux")]
    Mpris,
}
