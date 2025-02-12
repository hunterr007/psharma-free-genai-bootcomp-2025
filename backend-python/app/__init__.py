from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS

# Initialize extensions
db = SQLAlchemy()
ma = Marshmallow()

def create_app():
    """Initialize the core application."""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///words.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.url_map.strict_slashes = False  # Disable strict slashes globally
    
    # Initialize extensions
    db.init_app(app)
    ma.init_app(app)
    CORS(app)
    
    # Register blueprints
    from app.handlers import (
        words_bp,
        groups_bp,
        study_activities_bp,
        study_sessions_bp,
        dashboard_bp,
        reset_bp
    )
    
    app.register_blueprint(words_bp)
    app.register_blueprint(groups_bp)
    app.register_blueprint(study_activities_bp)
    app.register_blueprint(study_sessions_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(reset_bp)
    
    # Debug: print registered routes
    with app.app_context():
        print("Registered Routes:")
        for rule in app.url_map.iter_rules():
            print(f"{rule.endpoint}: {rule.rule}")
        
        db.create_all()
    
    return app
