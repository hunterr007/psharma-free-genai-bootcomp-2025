from app.models.models import StudySession, Word, Group, WordReviewItem
from datetime import datetime, timedelta
from sqlalchemy import func

class StudyService:
    @staticmethod
    def get_last_study_session():
        """Get the most recent study session."""
        return StudySession.query.order_by(StudySession.created_at.desc()).first()
    
    @staticmethod
    def get_study_progress():
        """Get study progress statistics."""
        total_words = Word.query.count()
        studied_words = Word.query\
            .join(WordReviewItem)\
            .distinct(Word.id)\
            .count()
        
        return {
            'total_words_studied': studied_words,
            'total_available_words': total_words
        }
    
    @staticmethod
    def get_quick_stats():
        """Get quick overview statistics."""
        # Calculate success rate
        total_reviews = WordReviewItem.query.count()
        correct_reviews = WordReviewItem.query.filter_by(correct=True).count()
        success_rate = (correct_reviews / total_reviews * 100) if total_reviews > 0 else 0
        
        # Get total study sessions
        total_sessions = StudySession.query.count()
        
        # Get total active groups (groups with at least one study session)
        active_groups = Group.query\
            .join(StudySession)\
            .distinct(Group.id)\
            .count()
        
        # Calculate study streak
        today = datetime.utcnow().date()
        streak = 0
        current_date = today
        
        while True:
            session_exists = StudySession.query\
                .filter(func.date(StudySession.created_at) == current_date)\
                .first() is not None
            
            if not session_exists:
                break
                
            streak += 1
            current_date -= timedelta(days=1)
        
        return {
            'success_rate': success_rate,
            'total_study_sessions': total_sessions,
            'total_active_groups': active_groups,
            'study_streak_days': streak
        }

    @staticmethod
    def create_study_session(group_id):
        """Create a new study session for a group."""
        study_session = StudySession(group_id=group_id)
        db.session.add(study_session)
        
        study_activity = StudyActivity(
            group_id=group_id,
            study_session=study_session
        )
        db.session.add(study_activity)
        
        db.session.commit()
        return study_session

    @staticmethod
    def record_word_review(word_id, study_session_id, correct):
        """Record a word review result."""
        review = WordReviewItem(
            word_id=word_id,
            study_session_id=study_session_id,
            correct=correct
        )
        db.session.add(review)
        db.session.commit()
        return review
