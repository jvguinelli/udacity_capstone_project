import os

from flask import (
    Flask,
    jsonify,
    render_template
)

from .companies import companies_blueprint
from .partners import partners_blueprint
from .sanctions import sanctions_blueprint

from .database.models import setup_db
from .auth.auth import AuthError


def create_app(test_config=None):
    app = Flask(__name__)

    app.register_blueprint(companies_blueprint)
    app.register_blueprint(partners_blueprint)
    app.register_blueprint(sanctions_blueprint)

    if test_config:
        app.config.from_mapping(test_config)
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = \
            os.getenv('SQLALCHEMY_DATABASE_URI')
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = \
            os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')

    setup_db(app)

    @app.route('/', methods=['GET'])
    def index():
        return jsonify({
            'message':
            'Welcome to Udacity Capstone Project - Sanctioned Companies API!'
        })

    @app.route('/show_created_token', methods=['GET'])
    def show_created_token():
        return render_template("show_created_token.html")

    # ERROR HANDLER

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            "success": False,
            "error": str(error.status_code),
            "message": error.error['description']
        }), error.status_code

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400,

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "not found"
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
        }), 500

    return app
