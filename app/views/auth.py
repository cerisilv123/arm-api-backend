from flask import request
from functools import wraps

# Decorator function to check for cross-origin requests
def preflight_check(f):
    """
    Decorator for adding CORS header check to preflight (OPTIONS) requests and forwarding
    other requests to the original view function. It enables cross-origin requests
    from specified domains such as localhost by adding necessary CORS response headers.

    Parameters:
    - f (function): The view function to wrap.

    Returns:
    - function: The decorated function with preflight OPTIONS handling.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        # Handle preflight requests for CORS by setting appropriate headers
        if request.method == 'OPTIONS':
            headers = {
                'Access-Control-Allow-Origin': 'http://localhost:3000',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type, Authorization, Refresh-Token',
                "Access-Control-Allow-Credentials": True
            }
            return ('', 204, headers)
        else:
            # For non-OPTIONS requests, call the original function
            return f(*args, **kwargs)

    return decorated