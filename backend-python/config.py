import os

class Config:
    # SQLite database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///words.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-please-change-in-production'
    
    # API settings
    JSON_SORT_KEYS = False
