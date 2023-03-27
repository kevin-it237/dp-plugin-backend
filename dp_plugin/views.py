
from flask import Blueprint, current_app, jsonify, abort, request, json
import sys
from werkzeug.local import LocalProxy
from datetime import date, datetime
from .config import config
from dotenv import load_dotenv
from . import get_environment
from werkzeug.utils import secure_filename
import base64
import os

from pymisp import MISPEvent, MISPObject, PyMISP

load_dotenv()

APPLICATION_ENV = get_environment()

MISP_DEBUG = config[APPLICATION_ENV] == "development"
misp = PyMISP(config[APPLICATION_ENV].MISP_URL, config[APPLICATION_ENV].API_KEY, True, debug=MISP_DEBUG)

misp.toggle_global_pythonify()  # Returns PyMISP objects whenever possible, allows to skip pythonify

core = Blueprint('core', __name__)
logger = LocalProxy(lambda: current_app.logger)

app_root = os.path.realpath(os.path.dirname(__file__))
template_url = os.path.join(app_root, "", "")
#template_definition = json.load(open(json_url))

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
        event.info = 'dark-pattern-1'  # Required
        # Optional, defaults to MISP.default_event_distribution in MISP config
        event.distribution = 0
        # Optional, defaults to MISP.default_event_threat_level in MISP config
        event.threat_level_id = 2
        event.analysis = 1  # Optional, defaults to 0 (initial analysis)
        event.published = True
        # add datetime attribute
        event.add_attribute(type='datetime', value=datetime.now())
        event.set_date(date.today())
        event.add_tag('dark-pattern-1')
        
        # Add custom object to the event
        #template = misp.get_object_template(297, pythonify=True).to_dict()
        #dark_pattern_v3_obj = MISPObject(name='dark-pattern-schema-v3', strict=False, misp_objects_template_custom=template)
        dark_pattern_v5_obj = MISPObject(name='dark-pattern-schema-v5', strict=True, misp_objects_path_custom=template_url)
        dark_pattern_v5_obj.add_attribute(object_relation='Place_of_publication', type='text', value="Blog")  #REQUIRED
        dark_pattern_v5_obj.add_attribute(object_relation='Regulations', type='text', value="Digital services act") #REQUIRED
        dark_pattern_v5_obj.add_attribute(object_relation='Dark pattern strategies', type='text', value=strategies)
        dark_pattern_v5_obj.add_attribute(object_relation='Data protection requirement', type='text', value=requirements)
        dark_pattern_v5_obj.add_attribute(object_relation='Additional_Info', type='text', value=notes)
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
        
        event = misp.add_event(event, pythonify=True)
        event.publish()

        if isinstance(event, dict) and 'errors' in event:
            print('add_event failed: {}'.format(event['errors']), file=sys.stderr)
            abort(422, description='add_event failed: {}'.format(event['errors']))

        return jsonify({
            'success': True,
            'created': json.dumps(event.to_json()),
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
