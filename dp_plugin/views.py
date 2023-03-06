
from flask import Blueprint, current_app, jsonify, abort, request
from werkzeug.local import LocalProxy
from datetime import date
from .config import config
from dotenv import load_dotenv
from . import get_environment
from werkzeug.utils import secure_filename
import json

from pymisp import MISPEvent, MISPObject, PyMISP

load_dotenv()

APPLICATION_ENV = get_environment()

MISP_DEBUG = config[APPLICATION_ENV] == "development"
misp = PyMISP(config[APPLICATION_ENV].MISP_URL, config[APPLICATION_ENV].API_KEY, True, debug=MISP_DEBUG)

misp.toggle_global_pythonify()  # Returns PyMISP objects whenever possible, allows to skip pythonify

core = Blueprint('core', __name__)
logger = LocalProxy(lambda: current_app.logger)

@core.before_request
def before_request_func():
    current_app.logger.name = 'core'

@core.route('/events', methods=['POST'])
def create_event():
    data = dict(request.form)
    error = ''
    try:
        if 'domain' not in data or data['domain'] is None:
            error = "domain name is missing"
            raise Exception(error)
        
        if 'location' not in data or data['location'] is None:
            error = "location is missing"
            raise Exception(error)
        
        if 'strategies' not in data or data['strategies'] is None:
            error = "strategies are missing"
            raise Exception(error)
        
        if 'attachment' not in request.files:
            error = "attachment is missing"
            raise Exception(error)
        
        if 'notes' not in data:
            error = "notes attribute is missing"
            raise Exception(error)
        
        if 'requirements' not in data:
            error = "requirements attribute is missing"
            raise Exception(error)
    except:
        abort(400, description=error)

    domain = data['domain']
    location = data['location']
    notes = data['notes'] 
    strategies = json.loads(data['strategies'])
    requirements = json.loads(data['requirements'])
    
    try:
        event = MISPEvent()
        event.info = 'dark-pattern-1'  # Required
        # Optional, defaults to MISP.default_event_distribution in MISP config
        event.distribution = 0
        # Optional, defaults to MISP.default_event_threat_level in MISP config
        event.threat_level_id = 2
        event.analysis = 1  # Optional, defaults to 0 (initial analysis)
        # event.published = True
        event.add_attribute(type='url', value=domain)
        event.add_attribute(type='other', value=location)
        event.set_date(date.today())
        event.add_tag('dark-pattern-1')
        # Add custom object to the event
        misp_object = MISPObject('custom-dark-pattern')
        # * standalone: this object will be attached to a MISPEvent, so the references will be in the dump
        misp_object.add_attribute('location',type='text', value=location)
        misp_object.add_attribute('requirements', type='text', value=requirements)
        misp_object.add_attribute('strategies', type='text', value=strategies)
        misp_object.add_attribute('notes', type='text', value=notes)
        event.add_object(misp_object)

        # Add an attachment
        # check if the post request has the file part
        file = dict(request.files)['attachment']
        filename = secure_filename(file.filename)
        # image_object = MISPObject('image')
        # image_object.add_attribute("attachment", value=filename, data=file, expand='binary')
        # image_object.add_attribute("filename", filename)
        # image_object.add_attribute("md5", file.md5)
        # image_object.add_attribute("sha1", file.sha1)
        # image_object.add_attribute("sha256", file.sha256)
        # event.add_object(image_object)
        event.publish()
        event = misp.add_event(event, pythonify=True)

        return jsonify({
            'success': True,
            'created': json.dumps(event.to_json()),
            'message': "Event successfully created",
        }), 201
    
    except Exception as e:
      abort(422, description=str(e))

@core.route('/events/<string:event_id>')
def get_events_by_id(event_id):
    if event_id is None:
      abort(404, description="Not found")
    return event_id
    
@core.route('/test', methods=['GET'])
def test():
    logger.info('app test route hit')
    return 'Congratulations! Your core-app test route is running!'
