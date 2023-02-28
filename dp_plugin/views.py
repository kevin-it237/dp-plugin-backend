
from flask import Blueprint, current_app, jsonify
from werkzeug.local import LocalProxy

core = Blueprint('core', __name__)
logger = LocalProxy(lambda: current_app.logger)

@core.before_request
def before_request_func():
    current_app.logger.name = 'core'

@core.route('/', methods=['GET'])
def hello_world():
    return jsonify({'message': 'Hello, World!'})

@core.route('/entrees/<int:entree_id>')
def retrieve_entree(entree_id):
    return 'Entree %d' % entree_id
    
@core.route('/test', methods=['GET'])
def test():
    logger.info('app test route hit')
    return 'Congratulations! Your core-app test route is running!'
