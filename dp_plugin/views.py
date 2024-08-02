# Copyright (c) 2024 Abel Kevin Ngaleu, University of Luxembourg
# This software is licensed under the MIT License.
# See the LICENSE file for more details.

from flask import Blueprint, current_app, jsonify, abort, request, json
import sys
from werkzeug.local import LocalProxy
from datetime import date, datetime
from .config import config
from .helper import build_misp_object
from dotenv import load_dotenv
from . import get_environment
from werkzeug.utils import secure_filename
import base64
import os

from pymisp import MISPEvent, MISPObject, PyMISP

load_dotenv()

APPLICATION_ENV = get_environment()

MISP_DEBUG = config[APPLICATION_ENV] == "development"
#misp = PyMISP(config[APPLICATION_ENV].MISP_URL, config[APPLICATION_ENV].API_KEY, ssl=True, debug=MISP_DEBUG)
misp = PyMISP("https://host.docker.internal", "MIjvBVzm3a32bl2gUDJvF3LSxNH57n7uLTy1nSUl", ssl=False, debug=True)

# misp.toggle_global_pythonify()  # Returns PyMISP objects whenever possible, allows to skip pythonify
#print(config[APPLICATION_ENV].MISP_URL)
core = Blueprint('core', __name__)
logger = LocalProxy(lambda: current_app.logger)

app_root = os.path.realpath(os.path.dirname(__file__))
template_url = os.path.join(app_root, "dark-patterns-v5", "definition.json")
template_definition = json.load(open(template_url))

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
    strategies = data['strategies']
    requirements = data['requirements']
    
    try:
        event = MISPEvent()
        event.info = 'dark-pattern-plugin'  # Required
        # Optional, defaults to MISP.default_event_distribution in MISP config
        event.distribution = 1
        # Optional, defaults to MISP.default_event_threat_level in MISP config
        event.threat_level_id = 1
        event.analysis = 1  # Optional, defaults to 0 (initial analysis)
        event.published = True
        # add datetime attribute
        event.add_attribute(type='datetime', value=datetime.now())
        event.add_attribute(type='target-location', value=location)
        event.set_date(date.today())
        event.add_tag('dark-pattern-plugin-1')
        
        # Add custom object to the event
        dark_pattern_v5_obj = MISPObject(name='dark-pattern-schema-v5', strict=False, misp_objects_template_custom=template_definition)
        dark_pattern_v5_obj.add_attribute(object_relation='Dark pattern strategies', type='text', value=strategies)
        dark_pattern_v5_obj.add_attribute(object_relation='Data protection requirement', type='text', value=requirements)
        dark_pattern_v5_obj.add_attribute(object_relation='Additional_Info', type='text', value=notes)
        
        # Add more dark pattern features to the event
        dark_pattern_v5_obj = build_misp_object(dark_pattern_v5_obj, data)
        
        event.add_object(dark_pattern_v5_obj)

        # Add an attachment
        # check if the post request has the file part
        file = dict(request.files)['attachment']
        image_string = base64.b64encode(file.read())
        filename = secure_filename(file.filename)
        attachment_object = MISPObject(name='image')
        attachment_object.add_attribute(object_relation="attachment", value=filename, data=image_string)
        attachment_object.add_attribute(object_relation="url", value=domain)
        event.add_object(attachment_object)
        
        created_event = misp.add_event(event, pythonify=False)

        if isinstance(event, dict) and 'errors' in event:
            print('add_event failed: {}'.format(event['errors']), file=sys.stderr)
            abort(422, description='add_event failed: {}'.format(event['errors']))

        return jsonify({
            'success': True,
            'message': "Event successfully created",
        }), 201
    
    except Exception as e:
      print(e)
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