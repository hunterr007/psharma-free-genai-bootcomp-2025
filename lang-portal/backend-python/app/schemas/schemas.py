from marshmallow import fields
from app import ma
from app.models.models import (
    Word,
    Group,
    StudyActivity,
    StudySession,
    WordReviewItem
)

class WordSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Word
    
    id = ma.auto_field()
    japanese = ma.auto_field()
    romaji = ma.auto_field()
    english = ma.auto_field()
    parts = ma.auto_field()
    correct_count = fields.Int()
    wrong_count = fields.Int()

class GroupSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Group
    
    id = ma.auto_field()
    name = ma.auto_field()
    word_count = fields.Int()
    stats = fields.Dict()

class StudyActivitySchema(ma.SQLAlchemySchema):
    class Meta:
        model = StudyActivity
    
    id = ma.auto_field()
    name = ma.auto_field()
    thumbnail_url = ma.auto_field()
    description = ma.auto_field()

class StudySessionSchema(ma.SQLAlchemySchema):
    class Meta:
        model = StudySession
    
    id = ma.auto_field()
    group_id = ma.auto_field()
    study_activity_id = ma.auto_field()
    created_at = ma.auto_field()
    activity = fields.Nested(StudyActivitySchema)
    review_items_count = fields.Int()

class WordReviewItemSchema(ma.SQLAlchemySchema):
    class Meta:
        model = WordReviewItem
    
    id = ma.auto_field()
    word_id = ma.auto_field()
    study_session_id = ma.auto_field()
    correct = ma.auto_field()
    created_at = ma.auto_field()
    word = fields.Nested(WordSchema)

class PaginationSchema(ma.Schema):
    has_next = fields.Bool()
    has_prev = fields.Bool()
    page = fields.Int()
    pages = fields.Int()
    total = fields.Int()

# Initialize schemas
word_schema = WordSchema()
words_schema = WordSchema(many=True)

group_schema = GroupSchema()
groups_schema = GroupSchema(many=True)

study_activity_schema = StudyActivitySchema()
study_activities_schema = StudyActivitySchema(many=True)

study_session_schema = StudySessionSchema()
study_sessions_schema = StudySessionSchema(many=True)

word_review_item_schema = WordReviewItemSchema()
word_review_items_schema = WordReviewItemSchema(many=True)

pagination_schema = PaginationSchema()

# Dashboard specific schemas
class DashboardLastStudySessionSchema(ma.Schema):
    id = fields.Int()
    group_id = fields.Int()
    group_name = fields.Str()
    activity_name = fields.Str()
    start_time = fields.DateTime()
    end_time = fields.DateTime()
    review_items_count = fields.Int()

class DashboardStatsSchema(ma.Schema):
    total_words = fields.Int()
    total_groups = fields.Int()
    total_study_sessions = fields.Int()
    total_review_items = fields.Int()
    total_correct_reviews = fields.Int()
    total_wrong_reviews = fields.Int()
    success_rate = fields.Float()

dashboard_last_study_session_schema = DashboardLastStudySessionSchema()
dashboard_stats_schema = DashboardStatsSchema()
