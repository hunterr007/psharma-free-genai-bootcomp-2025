from flask import jsonify
from app.handlers import dashboard_bp
from app.models.models import Word, Group, StudySession, WordReviewItem
from sqlalchemy import func
from datetime import datetime, timedelta

@dashboard_bp.route('/last_study_session', methods=['GET'])
def get_last_study_session():
    """Get the most recent study session."""
    last_session = (StudySession.query
                    .join(StudySession.activity)
                    .join(StudySession.group)
                    .order_by(StudySession.created_at.desc())
                    .first())
    
    if not last_session:
        return jsonify(None), 404
    
    return jsonify({
        'id': last_session.id,
        'group_id': last_session.group_id,
        'created_at': last_session.created_at.isoformat(),
        'study_activity_id': last_session.study_activity_id,
        'group_name': last_session.group.name
    })

@dashboard_bp.route('/study_progress', methods=['GET'])
def get_study_progress():
    """Get study progress statistics."""
    total_words_studied = WordReviewItem.query.count()
    total_available_words = Word.query.count()
    
    return jsonify({
        'total_words_studied': total_words_studied,
        'total_available_words': total_available_words
    })

@dashboard_bp.route('/quick-stats', methods=['GET'])
def get_quick_stats():
    """Get quick overview statistics."""
    # Calculate success rate
    total_reviews = WordReviewItem.query.count()
    correct_reviews = WordReviewItem.query.filter_by(correct=True).count()
    success_rate = (correct_reviews / total_reviews * 100) if total_reviews > 0 else 0
    
    # Total study sessions
    total_study_sessions = StudySession.query.count()
    
    # Total active groups
    total_active_groups = Group.query.count()
    
    # Study streak (consecutive days with at least one study session)
    today = datetime.utcnow().date()
    study_streak = 0
    current_date = today
    
    while True:
        sessions_on_date = StudySession.query.filter(
            func.date(StudySession.created_at) == current_date
        ).count()
        
        if sessions_on_date > 0:
            study_streak += 1
            current_date -= timedelta(days=1)
        else:
            break
    
    return jsonify({
        'success_rate': round(success_rate, 1),
        'total_study_sessions': total_study_sessions,
        'total_active_groups': total_active_groups,
        'study_streak_days': study_streak
    })
