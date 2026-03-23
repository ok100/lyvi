use std::time::Duration;

#[derive(Debug)]
pub struct LyricLine {
    timestamp: Duration,
    pub text: String,
}

#[derive(Default, Debug)]
pub enum Lyrics {
    #[default]
    Loading,
    Found(Vec<LyricLine>),
    NotFound,
    Failed(String),
}

impl Lyrics {
    pub fn new_found(mut lines: Vec<LyricLine>) -> Self {
        if lines.is_empty() {
            return Self::NotFound;
        }
        lines.sort_by_key(|line| line.timestamp);
        Self::Found(lines)
    }

    pub fn current_line_index(&self, position: Duration) -> Option<usize> {
        if let Self::Found(lines) = self {
            let index = lines.partition_point(|line| line.timestamp <= position);
            index.checked_sub(1)
        } else {
            None
        }
    }
}
