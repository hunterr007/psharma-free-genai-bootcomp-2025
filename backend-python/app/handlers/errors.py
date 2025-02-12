from flask import jsonify
from app import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from marshmallow import ValidationError

def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({
            'error': 'Not Found',
            'message': 'The requested resource was not found'
        }), 404

    @app.errorhandler(ValidationError)
    def validation_error(error):
        return jsonify({
            'error': 'Validation Error',
            'message': error.messages
        }), 400

    @app.errorhandler(IntegrityError)
    def integrity_error(error):
        db.session.rollback()
        return jsonify({
            'error': 'Database Error',
            'message': 'Database integrity error occurred'
        }), 400

    @app.errorhandler(SQLAlchemyError)
    def database_error(error):
        db.session.rollback()
        return jsonify({
            'error': 'Database Error',
            'message': 'A database error occurred'
        }), 500

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'An internal server error occurred'
        }), 500

    @app.errorhandler(Exception)
    def unhandled_error(error):
        db.session.rollback()
        return jsonify({
            'error': 'Unhandled Error',
            'message': 'An unexpected error occurred'
        }), 500
