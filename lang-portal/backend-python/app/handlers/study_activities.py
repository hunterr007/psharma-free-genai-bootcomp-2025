from flask import Blueprint, jsonify, request
from app.models.models import StudyActivity, StudySession, Group
from app.schemas.schemas import (
    study_activity_schema,
    study_activities_schema,
    study_session_schema,
    study_sessions_schema,
    pagination_schema
)
from app import db

study_activities_bp = Blueprint('study_activities', __name__, url_prefix='/api/study-activities')

@study_activities_bp.route('', methods=['GET'])
def get_study_activities():
    """Get all study activities."""
    activities = StudyActivity.query.all()
    return jsonify(study_activities_schema.dump(activities))

@study_activities_bp.route('/<int:activity_id>', methods=['GET'])
def get_study_activity(activity_id):
    """Get a specific study activity by ID."""
    activity = StudyActivity.query.get_or_404(activity_id)
    return jsonify({
        'id': activity.id,
        'name': activity.name,
        'description': activity.description or '',
        'thumbnail_url': activity.thumbnail_url or ''
    })

@study_activities_bp.route('/<int:activity_id>/study_sessions', methods=['GET'])
def get_study_activity_sessions(activity_id):
    """Get study sessions for a specific activity."""
    page = request.args.get('page', 1, type=int)
    per_page = 100
    
    # Ensure activity exists
    StudyActivity.query.get_or_404(activity_id)
    
    pagination = StudySession.query.filter_by(study_activity_id=activity_id)\
        .order_by(StudySession.created_at.desc())\
        .paginate(page=page, per_page=per_page)
    
    return jsonify({
        'items': study_sessions_schema.dump(pagination.items),
        'pagination': pagination_schema.dump(pagination)
    })

@study_activities_bp.route('', methods=['POST'])
def create_study_activity():
    """Create a new study activity."""
    data = request.get_json()
    
    # Create new study activity
    activity = StudyActivity(
        name=data.get('name'),
        thumbnail_url=data.get('thumbnail_url', ''),
        description=data.get('description', '')
    )
    
    db.session.add(activity)
    db.session.commit()
    
    return jsonify({
        'id': activity.id,
        'name': activity.name,
        'description': activity.description,
        'thumbnail_url': activity.thumbnail_url
    }), 201
