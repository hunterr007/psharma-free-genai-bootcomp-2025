package service

import (
	"database/sql"
	"fmt"
	"lang-portal/internal/models"
	"time"
)

type StudyActivitiesService struct {
	db *models.DB
}

func NewStudyActivitiesService(db *models.DB) *StudyActivitiesService {
	return &StudyActivitiesService{db: db}
}

func (s *StudyActivitiesService) GetStudyActivity(id int) (map[string]interface{}, error) {
	query := `
		SELECT id, name, COALESCE(thumbnail_url, '') as thumbnail_url, 
		       'Practice your vocabulary with flashcards' as description
		FROM study_activities
		WHERE id = ?
	`
	activity := make(map[string]interface{})
	var (
		activityID int
		name, thumbnailURL, description string
	)
	err := s.db.QueryRow(query, id).Scan(
		&activityID, 
		&name, 
		&thumbnailURL,
		&description,
	)
	if err == sql.ErrNoRows {
		return nil, fmt.Errorf("study activity not found")
	}
	if err != nil {
		return nil, err
	}
	activity["id"] = activityID
	activity["name"] = name
	activity["thumbnail_url"] = thumbnailURL
	activity["description"] = description
	return activity, nil
}

func (s *StudyActivitiesService) GetStudyActivitySessions(activityID, page int) ([]map[string]interface{}, *models.Pagination, error) {
	const itemsPerPage = 100
	offset := (page - 1) * itemsPerPage

	// Query to get total pages and items
	var totalItems int
	err := s.db.QueryRow(`
		SELECT COUNT(*) 
		FROM study_sessions 
		WHERE study_activity_id = ?
	`, activityID).Scan(&totalItems)
	if err != nil {
		return nil, nil, err
	}

	// Calculate total pages
	totalPages := (totalItems + itemsPerPage - 1) / itemsPerPage

	// Query to get sessions
	rows, err := s.db.Query(`
		SELECT 
			ss.id, 
			sa.name as activity_name, 
			g.name as group_name, 
			ss.created_at,
			(SELECT COUNT(*) FROM word_review_items wri WHERE wri.study_session_id = ss.id) as review_items_count
		FROM study_sessions ss
		JOIN study_activities sa ON ss.study_activity_id = sa.id
		JOIN groups g ON ss.group_id = g.id
		WHERE ss.study_activity_id = ?
		ORDER BY ss.created_at DESC
		LIMIT ? OFFSET ?
	`, activityID, itemsPerPage, offset)
	if err != nil {
		return nil, nil, err
	}
	defer rows.Close()

	var sessions []map[string]interface{}
	for rows.Next() {
		session := make(map[string]interface{})
		var (
			id int
			activityName, groupName string
			startTime time.Time
			reviewItemsCount int
		)
		err := rows.Scan(
			&id,
			&activityName,
			&groupName,
			&startTime,
			&reviewItemsCount,
		)
		if err != nil {
			return nil, nil, err
		}
		session["id"] = id
		session["activity_name"] = activityName
		session["group_name"] = groupName
		session["start_time"] = startTime
		session["end_time"] = startTime // Simplified for this example
		session["review_items_count"] = reviewItemsCount
		sessions = append(sessions, session)
	}

	pagination := &models.Pagination{
		CurrentPage:  page,
		TotalPages:   totalPages,
		TotalItems:   totalItems,
		ItemsPerPage: itemsPerPage,
	}

	return sessions, pagination, nil
}

func (s *StudyActivitiesService) CreateStudySession(groupID, activityID int) (*models.StudySession, error) {
	// Verify group and activity exist
	if err := s.verifyGroupAndActivity(groupID, activityID); err != nil {
		return nil, err
	}

	query := `
		INSERT INTO study_sessions (group_id, study_activity_id, created_at)
		VALUES (?, ?, CURRENT_TIMESTAMP)
		RETURNING id, group_id, created_at, study_activity_id
	`

	var session models.StudySession
	err := s.db.QueryRow(query, groupID, activityID).Scan(
		&session.ID,
		&session.GroupID,
		&session.CreatedAt,
		&session.StudyActivityID,
	)
	if err != nil {
		return nil, err
	}

	return &session, nil
}

func (s *StudyActivitiesService) verifyGroupAndActivity(groupID, activityID int) error {
	// Check if group exists
	var groupExists bool
	if err := s.db.QueryRow("SELECT EXISTS(SELECT 1 FROM groups WHERE id = ?)", groupID).Scan(&groupExists); err != nil {
		return err
	}
	if !groupExists {
		return fmt.Errorf("group with ID %d does not exist", groupID)
	}

	// Check if activity exists
	var activityExists bool
	if err := s.db.QueryRow("SELECT EXISTS(SELECT 1 FROM study_activities WHERE id = ?)", activityID).Scan(&activityExists); err != nil {
		return err
	}
	if !activityExists {
		return fmt.Errorf("study activity with ID %d does not exist", activityID)
	}

	return nil
}
