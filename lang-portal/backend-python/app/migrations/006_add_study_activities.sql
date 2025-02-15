-- Insert sample study activities
INSERT INTO study_activities (name, thumbnail_url, description) VALUES
    ('Vocabulary Quiz', 'https://example.com/vocab.jpg', 'Test your vocabulary knowledge'),
    ('Writing Practice', 'https://example.com/writing.jpg', 'Practice writing Japanese characters'),
    ('Listening Exercise', 'https://example.com/listening.jpg', 'Practice listening comprehension');

-- Insert sample study sessions
INSERT INTO study_sessions (group_id, study_activity_id, created_at) VALUES
    (1, 1, datetime('now', '-2 days')),
    (1, 2, datetime('now', '-1 day')),
    (2, 1, datetime('now'));
