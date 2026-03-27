use std::time::Duration;

#[derive(Debug)]
pub struct LyricLine {
    timestamp: Duration,
    pub text: String,
}

impl LyricLine {
    pub fn new(timestamp: Duration, text: &str) -> Self {
        LyricLine {
            timestamp,
            text: text.into(),
        }
    }
}

#[derive(Debug)]
pub struct LyricLines {
    lines: Vec<LyricLine>,
}

impl LyricLines {
    pub fn current_index(&self, position: Duration) -> Option<usize> {
        self.lines
            .partition_point(|l| l.timestamp <= position)
            .checked_sub(1)
    }
}

#[derive(Default, Debug)]
pub enum Lyrics {
    #[default]
    Loading,
    Found(LyricLines),
    NotFound,
    Failed(String),
}

impl From<Vec<LyricLine>> for Lyrics {
    fn from(mut lines: Vec<LyricLine>) -> Self {
        if lines.is_empty() {
            return Self::NotFound;
        }
        lines.sort_by_key(|l| l.timestamp);
        Self::Found(LyricLines { lines })
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::time::Duration;

    fn secs(secs: u64) -> Duration {
        Duration::from_secs(secs)
    }

    #[test]
    fn empty_vec_becomes_not_found() {
        let lines: Vec<LyricLine> = vec![];
        let lyrics = Lyrics::from(lines);
        assert!(matches!(lyrics, Lyrics::NotFound));
    }

    #[test]
    fn sorting_and_lrc_boundaries() {
        let lines = vec![
            LyricLine::new(secs(10), "Second"),
            LyricLine::new(secs(5), "First"),
            LyricLine::new(secs(15), "Third"),
        ];

        let lyrics = Lyrics::from(lines);

        let Lyrics::Found(lyric_lines) = &lyrics else {
            panic!("Should have been Found");
        };

        assert_eq!(lyric_lines.lines[0].timestamp.as_secs(), 5);
        assert_eq!(lyric_lines.lines[1].timestamp.as_secs(), 10);
        assert_eq!(lyric_lines.lines[2].timestamp.as_secs(), 15);

        assert_eq!(lyric_lines.current_index(secs(2)), None);
        assert_eq!(lyric_lines.current_index(secs(5)), Some(0));
        assert_eq!(lyric_lines.current_index(secs(7)), Some(0));
        assert_eq!(lyric_lines.current_index(secs(10)), Some(1));
        assert_eq!(lyric_lines.current_index(secs(100)), Some(2));
    }
}
