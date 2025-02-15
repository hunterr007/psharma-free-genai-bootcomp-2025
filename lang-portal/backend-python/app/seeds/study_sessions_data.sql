-- First, let's add some study activities if they don't exist
INSERT INTO study_activities (name, thumbnail_url, description) VALUES
    ('Vocabulary Flashcards', 'https://example.com/flashcards.jpg', 'Practice vocabulary with interactive flashcards'),
    ('Writing Practice', 'https://example.com/writing.jpg', 'Practice writing Japanese characters'),
    ('Listening Comprehension', 'https://example.com/listening.jpg', 'Improve your listening skills with audio exercises');

-- Add study sessions for different groups
INSERT INTO study_sessions (group_id, study_activity_id, created_at) VALUES
    -- Basic Greetings group sessions
    (1, 1, datetime('now', '-5 days')),
    (1, 2, datetime('now', '-3 days')),
    (1, 3, datetime('now', '-1 day')),
    
    -- Common Phrases group sessions
    (2, 1, datetime('now', '-4 days')),
    (2, 3, datetime('now', '-2 days')),
    
    -- Formal Speech group sessions
    (3, 2, datetime('now', '-1 day'));

-- Add word review items for these sessions
INSERT INTO word_review_items (word_id, study_session_id, correct, created_at) VALUES
    -- Reviews for Basic Greetings sessions
    (1, 1, 1, datetime('now', '-5 days')),  -- こんにちは - correct
    (4, 1, 0, datetime('now', '-5 days')),  -- おはよう - incorrect
    (1, 2, 1, datetime('now', '-3 days')),  -- こんにちは - correct
    (4, 2, 1, datetime('now', '-3 days')),  -- おはよう - correct
    (1, 3, 1, datetime('now', '-1 day')),   -- こんにちは - correct
    
    -- Reviews for Common Phrases sessions
    (2, 4, 1, datetime('now', '-4 days')),  -- ありがとう - correct
    (2, 5, 1, datetime('now', '-2 days')),  -- ありがとう - correct
    
    -- Reviews for Formal Speech sessions
    (3, 6, 1, datetime('now', '-1 day')),   -- さようなら - correct
    (3, 6, 0, datetime('now', '-1 day'));   -- さようなら - incorrect
