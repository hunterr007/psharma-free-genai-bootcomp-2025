from flask import Blueprint

# Create blueprints
words_bp = Blueprint('words', __name__, url_prefix='/api/words')
groups_bp = Blueprint('groups', __name__, url_prefix='/api/groups')
study_activities_bp = Blueprint('study_activities', __name__, url_prefix='/api/study-activities')
study_sessions_bp = Blueprint('study_sessions', __name__, url_prefix='/api/study-sessions')
dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/api/dashboard')
reset_bp = Blueprint('reset', __name__, url_prefix='/api/reset')

# Import handlers after creating blueprints to avoid circular imports
from app.handlers.words import *
from app.handlers.groups import *
from app.handlers.study_activities import *
from app.handlers.study_sessions import *
from app.handlers.dashboard import *
from app.handlers.reset import *
