package models

import (
	"database/sql"
	"log"
)

func MigrateDatabase(db *sql.DB) error {
	// Add thumbnail_url to study_activities
	_, err := db.Exec(`
		ALTER TABLE study_activities ADD COLUMN thumbnail_url TEXT;
		ALTER TABLE words ADD COLUMN correct_count INTEGER DEFAULT 0;
		ALTER TABLE words ADD COLUMN wrong_count INTEGER DEFAULT 0;

		-- Insert initial groups if not exists
		INSERT OR IGNORE INTO groups (name) VALUES 
		('Animals'),
		('Basic Greetings'),
		('Everyday Objects');

		-- Insert initial study activities if not exists
		INSERT OR IGNORE INTO study_activities (name, thumbnail_url) VALUES 
		('Vocabulary Quiz', 'https://example.com/quiz-thumbnail.jpg'),
		('Flashcard Practice', 'https://example.com/flashcard-thumbnail.jpg');

		-- Link initial words to groups
		INSERT OR IGNORE INTO words_groups (word_id, group_id)
		SELECT w.id, g.id
		FROM words w, groups g
		WHERE 
		(w.japanese = '犬' AND g.name = 'Animals') OR
		(w.japanese = '猫' AND g.name = 'Animals') OR
		(w.japanese = '鳥' AND g.name = 'Animals');
	`)
	if err != nil {
		log.Printf("Migration error: %v", err)
		return err
	}
	return nil
}
