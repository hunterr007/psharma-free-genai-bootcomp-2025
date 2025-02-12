package service

import (
	"database/sql"
	"time"

	"lang-portal/internal/models"
)

type DashboardService struct {
	db *models.DB
}

func NewDashboardService(db *models.DB) *DashboardService {
	return &DashboardService{db: db}
}

func (s *DashboardService) GetLastStudySession() (map[string]interface{}, error) {
	query := `
		SELECT id, group_id, created_at, study_activity_id, 
		       (SELECT name FROM groups WHERE id = study_sessions.group_id) as group_name
		FROM study_sessions
		ORDER BY created_at DESC
		LIMIT 1
	`
	session := make(map[string]interface{})
	var (
		id, groupID, studyActivityID int
		createdAt time.Time
		groupName string
	)
	err := s.db.QueryRow(query).Scan(
		&id, 
		&groupID, 
		&createdAt, 
		&studyActivityID, 
		&groupName,
	)
	if err == sql.ErrNoRows {
		session["id"] = 0
		session["group_id"] = 0
		session["created_at"] = time.Now()
		session["study_activity_id"] = 0
		session["group_name"] = "No recent sessions"
		return session, nil
	}
	if err != nil {
		return nil, err
	}
	session["id"] = id
	session["group_id"] = groupID
	session["created_at"] = createdAt
	session["study_activity_id"] = studyActivityID
	session["group_name"] = groupName
	return session, nil
}

func (s *DashboardService) GetStudyProgress() (map[string]interface{}, error) {
	var totalWords, studiedWords int
	
	// Get total available words
	err := s.db.QueryRow("SELECT COUNT(*) FROM words").Scan(&totalWords)
	if err != nil {
		return nil, err
	}
	
	// Get total studied words (with at least one correct review)
	err = s.db.QueryRow(`
		SELECT COUNT(DISTINCT word_id) 
		FROM word_review_items 
		WHERE correct = 1
	`).Scan(&studiedWords)
	if err != nil {
		studiedWords = 0
	}
	
	return map[string]interface{}{
		"total_words_studied": studiedWords,
		"total_available_words": totalWords,
	}, nil
}

func (s *DashboardService) GetQuickStats() (map[string]interface{}, error) {
	var totalSessions, activeGroups, successRate, wordsLearned, wordsInProgress int
	
	// Total study sessions
	err := s.db.QueryRow("SELECT COUNT(*) FROM study_sessions").Scan(&totalSessions)
	if err != nil {
		totalSessions = 0
	}
	
	// Active groups
	err = s.db.QueryRow("SELECT COUNT(*) FROM groups").Scan(&activeGroups)
	if err != nil {
		activeGroups = 0
	}
	
	// Success rate calculation
	err = s.db.QueryRow(`
		SELECT 
			CASE 
				WHEN COUNT(*) > 0 
				THEN (CAST(SUM(CASE WHEN correct = 1 THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*)) * 100 
				ELSE 0 
			END as success_rate,
			COUNT(DISTINCT word_id) as words_learned,
			COUNT(DISTINCT word_id) as words_in_progress
		FROM word_review_items
	`).Scan(&successRate, &wordsLearned, &wordsInProgress)
	if err != nil {
		successRate = 0
		wordsLearned = 0
		wordsInProgress = 0
	}
	
	return map[string]interface{}{
		"success_rate": successRate,
		"total_study_sessions": totalSessions,
		"total_active_groups": activeGroups,
		"study_streak_days": 0,  // TODO: Implement actual streak calculation
		"words_learned": wordsLearned,
		"words_in_progress": wordsInProgress,
	}, nil
}
