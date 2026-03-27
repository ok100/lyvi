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

#[derive(Default, Debug)]
pub enum Lyrics {
    #[default]
    Loading,
    Found(Vec<LyricLine>),
    NotFound,
    Failed(String),
}

impl From<Vec<LyricLine>> for Lyrics {
    fn from(mut lines: Vec<LyricLine>) -> Self {
        if lines.is_empty() {
            return Self::NotFound;
        }
        lines.sort_by_key(|line| line.timestamp);
        Self::Found(lines)
    }
}

impl Lyrics {
    pub fn current_line_index(&self, position: Duration) -> Option<usize> {
        let Self::Found(lines) = self else {
            return None;
        };
        let index = lines.partition_point(|line| line.timestamp <= position);
        index.checked_sub(1)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::time::Duration;

    #[test]
    fn empty_vec_becomes_not_found() {
        let lines: Vec<LyricLine> = vec![];
        let lyrics = Lyrics::from(lines);
        assert!(matches!(lyrics, Lyrics::NotFound));
    }

    #[test]
    fn sorting_and_lrc_boundaries() {
        let lines = vec![
            LyricLine::new(Duration::from_secs(10), "Second"),
            LyricLine::new(Duration::from_secs(5), "First"),
            LyricLine::new(Duration::from_secs(15), "Third"),
        ];

        let lyrics = Lyrics::from(lines);

        let Lyrics::Found(sorted_lines) = &lyrics else {
            panic!("Should have been Found");
        };

        assert_eq!(sorted_lines[0].timestamp.as_secs(), 5);
        assert_eq!(sorted_lines[1].timestamp.as_secs(), 10);
        assert_eq!(sorted_lines[2].timestamp.as_secs(), 15);

        assert_eq!(lyrics.current_line_index(Duration::from_secs(2)), None);
        assert_eq!(lyrics.current_line_index(Duration::from_secs(5)), Some(0));
        assert_eq!(lyrics.current_line_index(Duration::from_secs(7)), Some(0));
        assert_eq!(lyrics.current_line_index(Duration::from_secs(10)), Some(1));
        assert_eq!(lyrics.current_line_index(Duration::from_secs(100)), Some(2));
    }

    #[test]
    fn other_variants_return_none() {
        let loading = Lyrics::Loading;
        let failed = Lyrics::Failed("error".into());
        let not_found = Lyrics::NotFound;

        assert_eq!(loading.current_line_index(Duration::from_secs(5)), None);
        assert_eq!(failed.current_line_index(Duration::from_secs(5)), None);
        assert_eq!(not_found.current_line_index(Duration::from_secs(5)), None);
    }
}
