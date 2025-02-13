from datetime import datetime
from app import db

class Word(db.Model):
    __tablename__ = 'words'
    
    id = db.Column(db.Integer, primary_key=True)
    japanese = db.Column(db.String(100), nullable=False)
    romaji = db.Column(db.String(100), nullable=False)
    english = db.Column(db.String(100), nullable=False)
    parts = db.Column(db.String(500))  # JSON string
    
    groups = db.relationship('Group', secondary='words_groups', back_populates='words')
    review_items = db.relationship('WordReviewItem', back_populates='word')
    
    @property
    def correct_count(self):
        return sum(1 for item in self.review_items if item.correct)
    
    @property
    def wrong_count(self):
        return sum(1 for item in self.review_items if not item.correct)

class Group(db.Model):
    __tablename__ = 'groups'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    
    words = db.relationship('Word', secondary='words_groups', back_populates='groups')
    study_sessions = db.relationship('StudySession', back_populates='group')
    
    @property
    def word_count(self):
        return len(self.words)
    
    @property
    def stats(self):
        total_reviews = 0
        correct_reviews = 0
        
        for session in self.study_sessions:
            for review in session.review_items:
                total_reviews += 1
                if review.correct:
                    correct_reviews += 1
        
        return {
            'total_reviews': total_reviews,
            'correct_reviews': correct_reviews,
            'success_rate': (correct_reviews / total_reviews * 100) if total_reviews > 0 else 0
        }

class WordGroup(db.Model):
    __tablename__ = 'words_groups'
    
    id = db.Column(db.Integer, primary_key=True)
    word_id = db.Column(db.Integer, db.ForeignKey('words.id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)

class StudyActivity(db.Model):
    __tablename__ = 'study_activities'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    thumbnail_url = db.Column(db.String(500))
    description = db.Column(db.String(500))
    
    sessions = db.relationship('StudySession', back_populates='activity')

class StudySession(db.Model):
    __tablename__ = 'study_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)
    study_activity_id = db.Column(db.Integer, db.ForeignKey('study_activities.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    group = db.relationship('Group', back_populates='study_sessions')
    activity = db.relationship('StudyActivity', back_populates='sessions')
    review_items = db.relationship('WordReviewItem', back_populates='session')
    
    @property
    def activity_name(self):
        return self.activity.name if self.activity else None
    
    @property
    def group_name(self):
        return self.group.name if self.group else None
    
    @property
    def start_time(self):
        return self.created_at
    
    @property
    def end_time(self):
        if not self.review_items:
            return self.created_at
        return max(item.created_at for item in self.review_items)
    
    @property
    def review_items_count(self):
        return self.review_items.count()

class WordReviewItem(db.Model):
    __tablename__ = 'word_review_items'
    
    id = db.Column(db.Integer, primary_key=True)
    word_id = db.Column(db.Integer, db.ForeignKey('words.id'), nullable=False)
    study_session_id = db.Column(db.Integer, db.ForeignKey('study_sessions.id'), nullable=False)
    correct = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    word = db.relationship('Word', back_populates='review_items')
    session = db.relationship('StudySession', back_populates='review_items')
