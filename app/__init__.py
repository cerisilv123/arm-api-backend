import sys
import secrets
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

from app.response import Response

# Creating Flask app
app = Flask(__name__)
CORS(app) # Allow for cross-origin requests

@app.errorhandler(Exception)
def handle_exception(error):
    """
    Error handler for unhandled exceptions in the Flask app.

    Parameters:
        error (Exception): The unhandled exception object.

    Returns:
        tuple: A JSON body in the error response format in the 'Response' class.
    """
    error_message = str(error)
    response = Response(error_message, 401)
    return response.return_error_response()

def create_app():
    """
    Creates a Flask application by setting configuration details, registering API views, and blueprints.

    Returns:
        Flask: The Flask application instance.

    Raises:
        Exception: If an error occurs while creating the application, logs the exception using LogSnag and exits the program with status code 1.
    """
    try: 
        # 1) Loading envars from .env
        load_dotenv()
        
        # Configure app settings here
        app.config['DEBUG'] = True
        session_key = secrets.token_urlsafe(16)
        app.config["SECRET_KEY"] = f"{session_key}" 
        app.secret_key = session_key 

        # Register API routes and blueprints - FINISH THIS
        from app.views.mining import mining

        app.register_blueprint(mining, url_prefix='/arm/api')
        
        return app
    except Exception as e:
        sys.exit(1)

