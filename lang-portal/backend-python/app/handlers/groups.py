from flask import Blueprint, jsonify, request
from app.models.models import Group, Word, WordGroup
from app.schemas.schemas import group_schema, groups_schema, words_schema
from app import db

groups_bp = Blueprint('groups', __name__, url_prefix='/api/groups')

@groups_bp.route('', methods=['GET'])
def get_groups():
    """Get all groups."""
    groups = Group.query.all()
    return jsonify(groups_schema.dump(groups))

@groups_bp.route('/<int:group_id>', methods=['GET'])
def get_group(group_id):
    """Get a specific group by ID."""
    group = Group.query.get_or_404(group_id)
    return jsonify(group_schema.dump(group))

@groups_bp.route('/<int:group_id>/words', methods=['GET'])
def get_group_words(group_id):
    """Get words in a specific group."""
    group = Group.query.get_or_404(group_id)
    words = group.words
    return jsonify(words_schema.dump(words))

@groups_bp.route('', methods=['POST'])
def create_group():
    """Create a new group."""
    data = request.get_json()
    
    # Create new group
    group = Group(
        name=data.get('name')
    )
    
    db.session.add(group)
    db.session.commit()
    
    return jsonify(group_schema.dump(group)), 201

@groups_bp.route('/<int:group_id>', methods=['PUT'])
def update_group(group_id):
    """Update a specific group."""
    group = Group.query.get_or_404(group_id)
    data = request.get_json()
    group.name = data.get('name', group.name)
    db.session.commit()
    return jsonify(group_schema.dump(group))

@groups_bp.route('/<int:group_id>', methods=['DELETE'])
def delete_group(group_id):
    """Delete a specific group."""
    group = Group.query.get_or_404(group_id)
    db.session.delete(group)
    db.session.commit()
    return '', 204

@groups_bp.route('/<int:group_id>/words', methods=['POST'])
def add_word_to_group(group_id):
    """Add a word to a group."""
    data = request.get_json()
    word_id = data['word_id']
    
    # Ensure both group and word exist
    Group.query.get_or_404(group_id)
    Word.query.get_or_404(word_id)
    
    # Check if association already exists
    exists = WordGroup.query.filter_by(
        word_id=word_id,
        group_id=group_id
    ).first()
    
    if exists:
        return jsonify({'message': 'Word already in group'}), 400
    
    word_group = WordGroup(word_id=word_id, group_id=group_id)
    db.session.add(word_group)
    db.session.commit()
    
    return jsonify({'message': 'Word added to group'}), 201

@groups_bp.route('/<int:group_id>/words/<int:word_id>', methods=['DELETE'])
def remove_word_from_group(group_id, word_id):
    """Remove a word from a group."""
    word_group = WordGroup.query.filter_by(
        word_id=word_id,
        group_id=group_id
    ).first_or_404()
    
    db.session.delete(word_group)
    db.session.commit()
    return '', 204
