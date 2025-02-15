-- Drop existing tables
DROP TABLE IF EXISTS word_review_items;
DROP TABLE IF EXISTS study_sessions;
DROP TABLE IF EXISTS study_activities;
DROP TABLE IF EXISTS words_groups;
DROP TABLE IF EXISTS words;
DROP TABLE IF EXISTS groups;

-- Create tables with correct schema
CREATE TABLE groups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE words (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    japanese TEXT NOT NULL,
    romaji TEXT NOT NULL,
    english TEXT NOT NULL,
    parts TEXT
);

CREATE TABLE words_groups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    word_id INTEGER NOT NULL,
    group_id INTEGER NOT NULL,
    FOREIGN KEY (word_id) REFERENCES words(id),
    FOREIGN KEY (group_id) REFERENCES groups(id)
);

CREATE TABLE study_activities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    thumbnail_url TEXT,
    description TEXT
);

CREATE TABLE study_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    group_id INTEGER NOT NULL,
    study_activity_id INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (group_id) REFERENCES groups(id),
    FOREIGN KEY (study_activity_id) REFERENCES study_activities(id)
);

CREATE TABLE word_review_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    word_id INTEGER NOT NULL,
    study_session_id INTEGER NOT NULL,
    correct BOOLEAN NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (word_id) REFERENCES words(id),
    FOREIGN KEY (study_session_id) REFERENCES study_sessions(id)
);

-- Insert sample data
INSERT INTO study_activities (name, thumbnail_url, description) VALUES
    ('Vocabulary Quiz', 'https://example.com/vocab.jpg', 'Test your vocabulary knowledge'),
    ('Writing Practice', 'https://example.com/writing.jpg', 'Practice writing Japanese characters'),
    ('Listening Exercise', 'https://example.com/listening.jpg', 'Practice listening comprehension');

INSERT INTO groups (name) VALUES
    ('Basic Greetings'),
    ('Numbers'),
    ('Common Phrases');

INSERT INTO words (japanese, romaji, english, parts) VALUES
    ('こんにちは', 'konnichiwa', 'hello', '{"type": "greeting"}'),
    ('さようなら', 'sayounara', 'goodbye', '{"type": "greeting"}'),
    ('ありがとう', 'arigatou', 'thank you', '{"type": "expression"}');

INSERT INTO words_groups (word_id, group_id) VALUES
    (1, 1),  -- hello -> Basic Greetings
    (2, 1),  -- goodbye -> Basic Greetings
    (3, 3);  -- thank you -> Common Phrases

INSERT INTO study_sessions (group_id, study_activity_id, created_at) VALUES
    (1, 1, datetime('now', '-2 days')),
    (1, 2, datetime('now', '-1 day')),
    (3, 1, datetime('now'));

INSERT INTO word_review_items (word_id, study_session_id, correct, created_at) VALUES
    (1, 1, 1, datetime('now', '-2 days')),  -- hello - correct
    (2, 1, 0, datetime('now', '-2 days')),  -- goodbye - incorrect
    (1, 2, 1, datetime('now', '-1 day')),   -- hello - correct
    (3, 3, 1, datetime('now'));             -- thank you - correct
