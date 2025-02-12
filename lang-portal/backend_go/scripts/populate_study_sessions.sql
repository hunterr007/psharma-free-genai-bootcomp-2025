-- Insert study sessions
INSERT INTO study_sessions (group_id, study_activity_id, created_at) VALUES 
(5, 1, '2025-02-10 10:00:00'),
(5, 1, '2025-02-11 11:30:00'),
(6, 2, '2025-02-12 09:45:00');

-- Insert word review items for the first study session (Animals group, Vocabulary Quiz)
INSERT INTO word_review_items (word_id, study_session_id, correct, created_at) VALUES 
(10, 1, 1, '2025-02-10 10:05:00'),  -- 犬 (dog)
(11, 1, 0, '2025-02-10 10:10:00'),  -- 猫 (cat)
(12, 1, 1, '2025-02-10 10:15:00');  -- 鳥 (bird)

-- Insert word review items for the second study session (Animals group, Vocabulary Quiz)
INSERT INTO word_review_items (word_id, study_session_id, correct, created_at) VALUES 
(10, 2, 1, '2025-02-11 11:35:00'),  -- 犬 (dog)
(11, 2, 1, '2025-02-11 11:40:00'),  -- 猫 (cat)
(12, 2, 0, '2025-02-11 11:45:00');  -- 鳥 (bird)

-- Insert word review items for the third study session (Basic Words, Flashcard Practice)
INSERT INTO word_review_items (word_id, study_session_id, correct, created_at) VALUES 
(10, 3, 1, '2025-02-12 09:50:00'),  -- 犬 (dog)
(11, 3, 1, '2025-02-12 09:55:00');  -- 猫 (cat)
