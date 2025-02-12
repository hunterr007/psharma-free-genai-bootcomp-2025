-- Create study_activities table
CREATE TABLE IF NOT EXISTS study_activities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    thumbnail_url VARCHAR(500),
    description VARCHAR(500)
);

-- Insert some default study activities
INSERT INTO study_activities (name, thumbnail_url, description) VALUES
    ('Vocabulary Quiz', 'https://example.com/vocab-quiz.jpg', 'Practice your vocabulary with flashcards'),
    ('Writing Practice', 'https://example.com/writing.jpg', 'Practice writing Japanese characters'),
    ('Listening Exercise', 'https://example.com/listening.jpg', 'Improve your listening comprehension');

-- Add study_activity_id to study_sessions if it doesn't exist
ALTER TABLE study_sessions ADD COLUMN study_activity_id INTEGER REFERENCES study_activities(id);
