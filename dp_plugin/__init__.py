# Import your dependencies
from flask import Flask, jsonify
from flask_cors import CORS
from .config import config
from dotenv import load_dotenv
from os import environ
import logging.config

def create_app(test_config=None):
    # Create and configure the app
    # Include the first parameter: Here, __name__is the name of the current Python module.
    app = Flask(__name__, instance_relative_config=True)

    load_dotenv()
    APPLICATION_ENV = get_environment()

    logging.config.dictConfig(config[APPLICATION_ENV].LOGGING)

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,PUT,DELETE,OPTIONS')
        return response

    app.config.from_object(config[APPLICATION_ENV])

    @app.route('/', methods=['GET'])
    def hello_world():
        return jsonify({'message': 'Hello, World!'})

    @app.route('/entrees/<int:entree_id>')
    def retrieve_entree(entree_id):
        return 'Entree %d' % entree_id

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable"
        }), 404

    # Return the app instance
    return app

def get_environment():
    return environ.get('APPLICATION_ENV') or 'development'