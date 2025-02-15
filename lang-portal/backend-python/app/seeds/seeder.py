from app import db
from app.models.models import Word, Group, WordGroup, StudySession, StudyActivity, WordReviewItem
from datetime import datetime, timedelta

def seed_data():
    """Seed the database with sample data."""
    # Clear existing data
    WordReviewItem.query.delete()
    WordGroup.query.delete()
    StudyActivity.query.delete()
    StudySession.query.delete()
    Word.query.delete()
    Group.query.delete()
    
    # Create sample words
    words = [
        Word(
            japanese='こんにちは',
            romaji='konnichiwa',
            english='hello',
            parts='{"type": "greeting", "formality": "neutral"}'
        ),
        Word(
            japanese='ありがとう',
            romaji='arigatou',
            english='thank you',
            parts='{"type": "gratitude", "formality": "neutral"}'
        ),
        Word(
            japanese='さようなら',
            romaji='sayounara',
            english='goodbye',
            parts='{"type": "farewell", "formality": "formal"}'
        ),
        Word(
            japanese='おはよう',
            romaji='ohayou',
            english='good morning',
            parts='{"type": "greeting", "formality": "informal"}'
        )
    ]
    
    for word in words:
        db.session.add(word)
    
    # Create sample groups
    groups = [
        Group(name='Basic Greetings'),
        Group(name='Common Phrases'),
        Group(name='Formal Speech')
    ]
    
    for group in groups:
        db.session.add(group)
    
    db.session.commit()
    
    # Create word-group associations
    word_groups = [
        WordGroup(word_id=words[0].id, group_id=groups[0].id),
        WordGroup(word_id=words[1].id, group_id=groups[1].id),
        WordGroup(word_id=words[2].id, group_id=groups[2].id),
        WordGroup(word_id=words[3].id, group_id=groups[0].id)
    ]
    
    for word_group in word_groups:
        db.session.add(word_group)
    
    # Create study sessions and activities
    study_session = StudySession(group_id=groups[0].id)
    db.session.add(study_session)
    db.session.commit()
    
    study_activity = StudyActivity(
        study_session_id=study_session.id,
        group_id=groups[0].id
    )
    db.session.add(study_activity)
    
    # Create word reviews
    reviews = [
        WordReviewItem(
            word_id=words[0].id,
            study_session_id=study_session.id,
            correct=True,
            created_at=datetime.utcnow() - timedelta(minutes=30)
        ),
        WordReviewItem(
            word_id=words[3].id,
            study_session_id=study_session.id,
            correct=False,
            created_at=datetime.utcnow() - timedelta(minutes=15)
        )
    ]
    
    for review in reviews:
        db.session.add(review)
    
    db.session.commit()
    
    print("Sample data has been seeded successfully!")
