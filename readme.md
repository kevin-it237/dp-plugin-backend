# Dark pattern report

This project is a ..

All backend code follows [PEP8 style guidelines](https://www.python.org/dev/peps/pep-0008/). 

#### Backend

From the backend folder run `pip install requirements.txt`. All required packages are included in the requirements file. 

To run the application run the following commands: 
```
export FLASK_APP=dp_plugin
export FLASK_DEBUG=1
flask run
```

Or using the command
```
flask --app dp_plugin --debug run
```

Run production
```
gunicorn --workers=3  wsgi:app --daemon
```
cut process: 
sudo pkill -f gunicorn
sudo nginx -s reload

These commands put the application in development and directs our application to use the `__init__.py` file in our dp_plugin folder. Working in development mode shows an interactive debugger in the console and restarts the server whenever changes are made. If running locally on Windows, look for the commands in the [Flask documentation](http://flask.pocoo.org/docs/1.0/tutorial/factory/).

The application is run on `http://127.0.0.1:5000/` by default and is a proxy in the frontend configuration. 

## API Reference

### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration. 
- Authentication: This version of the application does not require authentication or API keys. 

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return three error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable 

### Endpoints 

#### POST /events
- General:
    - Create an event on MISP
```
{
  
}
```

# Getting Started

### Prerequisites

- Python 3.6.2 or higher

### Project setup
```sh
# clone the repo
$ git clone git@github.com:kevin-it237/dp-plugin-backend.git
# move to the project folder
$ cd dp-plugin-backend

### Creating virtual environment
- Install `pipenv` a global python project `pip install pipenv`
- Create a `virtual environment` for this project
```

#### Create a .env file at the root of the project
```
APPLICATION_ENV=development
APP_NAME=dp-plugin
API_KEY=YOUR_MISP_API_KEY
MISP_URL=yourmispinstance.domain
```
...