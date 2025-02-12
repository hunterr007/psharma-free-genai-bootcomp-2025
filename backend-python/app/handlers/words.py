from flask import Blueprint, jsonify, request
from app.models.models import Word, Group
from app.schemas.schemas import word_schema, words_schema
from app import db
import json

words_bp = Blueprint('words', __name__, url_prefix='/api/words')

@words_bp.route('', methods=['GET'])
def get_words():
    """Get all words."""
    words = Word.query.all()
    return jsonify(words_schema.dump(words))

@words_bp.route('/<int:word_id>', methods=['GET'])
def get_word(word_id):
    """Get a specific word by ID."""
    word = Word.query.get_or_404(word_id)
    return jsonify(word_schema.dump(word))

@words_bp.route('', methods=['POST'])
def create_word():
    """Create a new word."""
    data = request.get_json()
    
    # Create new word
    word = Word(
        japanese=data.get('japanese'),
        romaji=data.get('romaji'),
        english=data.get('english'),
        parts=json.dumps(data.get('parts', {})) if data.get('parts') else None
    )
    
    db.session.add(word)
    db.session.commit()
    
    return jsonify(word_schema.dump(word)), 201

@words_bp.route('/<int:word_id>', methods=['PUT'])
def update_word(word_id):
    """Update a word."""
    word = Word.query.get_or_404(word_id)
    data = request.get_json()
    
    word.japanese = data.get('japanese', word.japanese)
    word.romaji = data.get('romaji', word.romaji)
    word.english = data.get('english', word.english)
    word.parts = json.dumps(data.get('parts', {})) if data.get('parts') else None
    
    # Update groups if specified
    if 'group_ids' in data:
        groups = Group.query.filter(Group.id.in_(data['group_ids'])).all()
        word.groups = groups
    
    db.session.commit()
    
    return jsonify(word_schema.dump(word))

@words_bp.route('/<int:word_id>', methods=['DELETE'])
def delete_word(word_id):
    """Delete a word."""
    word = Word.query.get_or_404(word_id)
    db.session.delete(word)
    db.session.commit()
    return '', 204
