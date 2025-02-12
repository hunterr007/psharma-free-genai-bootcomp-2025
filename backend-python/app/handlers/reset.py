from flask import jsonify
from app.handlers import reset_bp
from app.models.models import StudySession, WordReviewItem, Word, Group, WordGroup
from app import db

@reset_bp.route('/history', methods=['POST'])
def reset_history():
    """Reset all study history."""
    # Delete all study sessions and word review items
    WordReviewItem.query.delete()
    StudySession.query.delete()
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Study history has been reset'
    })

@reset_bp.route('/full', methods=['POST'])
def full_reset():
    """Reset the entire system."""
    # Delete all data
    WordReviewItem.query.delete()
    StudySession.query.delete()
    WordGroup.query.delete()
    Word.query.delete()
    Group.query.delete()
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'System has been fully reset'
    })
