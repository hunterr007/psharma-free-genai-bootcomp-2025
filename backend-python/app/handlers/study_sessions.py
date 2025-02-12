from flask import Blueprint, jsonify, request
from app.models.models import StudySession, StudyActivity, Group, Word, WordReview
from app.schemas.schemas import (
    study_session_schema,
    study_sessions_schema,
    pagination_schema,
    word_review_schema
)
from app import db
from datetime import datetime

study_sessions_bp = Blueprint('study_sessions', __name__, url_prefix='/api/study-sessions', strict_slashes=False)

@study_sessions_bp.route('', methods=['GET'])
def get_study_sessions():
    """Get all study sessions with pagination."""
    page = request.args.get('page', 1, type=int)
    per_page = 100
    
    pagination = StudySession.query\
        .order_by(StudySession.created_at.desc())\
        .paginate(page=page, per_page=per_page)
    
    return jsonify({
        'items': study_sessions_schema.dump(pagination.items),
        'pagination': pagination_schema.dump(pagination)
    })

@study_sessions_bp.route('/<int:session_id>', methods=['GET'])
def get_study_session(session_id):
    """Get a specific study session by ID."""
    session = StudySession.query.get_or_404(session_id)
    
    # Get group name
    group_name = session.group.name if session.group else None
    
    return jsonify({
        'id': session.id,
        'created_at': session.created_at.isoformat(),
        'group_id': session.group_id,
        'group_name': group_name,
        'study_activity_id': session.study_activity_id,
        'review_items_count': session.word_reviews.count()
    })

@study_sessions_bp.route('/<int:session_id>/words', methods=['GET'])
def get_session_words(session_id):
    """Get words reviewed in a specific study session."""
    page = request.args.get('page', 1, type=int)
    per_page = 100
    
    # Ensure session exists
    StudySession.query.get_or_404(session_id)
    
    # Get words from review items
    pagination = Word.query\
        .join(WordReview)\
        .filter(WordReview.study_session_id == session_id)\
        .paginate(page=page, per_page=per_page)
    
    return jsonify({
        'items': words_schema.dump(pagination.items),
        'pagination': pagination_schema.dump(pagination)
    })

@study_sessions_bp.route('', methods=['POST'])
def create_study_session():
    """Create a new study session."""
    data = request.get_json()
    
    # Validate required fields
    study_activity_id = data.get('study_activity_id')
    group_id = data.get('group_id')
    
    # Ensure study activity and group exist
    StudyActivity.query.get_or_404(study_activity_id)
    Group.query.get_or_404(group_id)
    
    # Create new study session
    session = StudySession(
        study_activity_id=study_activity_id,
        group_id=group_id
    )
    
    db.session.add(session)
    db.session.commit()
    
    return jsonify({
        'id': session.id,
        'created_at': session.created_at.isoformat(),
        'group_id': session.group_id,
        'study_activity_id': session.study_activity_id
    }), 201

@study_sessions_bp.route('/<int:session_id>/word-reviews', methods=['POST'])
def create_word_review(session_id):
    """Create a word review for a study session."""
    data = request.get_json()
    
    # Validate required fields
    word_id = data.get('word_id')
    correct = data.get('correct', False)
    
    # Ensure session and word exist
    session = StudySession.query.get_or_404(session_id)
    word = Word.query.get_or_404(word_id)
    
    # Create word review
    review = WordReview(
        study_session_id=session_id,
        word_id=word_id,
        correct=correct
    )
    
    db.session.add(review)
    db.session.commit()
    
    return jsonify({
        'study_session_id': session_id,
        'word_id': word_id,
        'correct': correct,
        'success': correct,
        'created_at': review.created_at.isoformat()
    }), 200
