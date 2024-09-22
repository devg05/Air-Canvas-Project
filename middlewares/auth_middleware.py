''' Code to check if user is autheticated or not'''

from functools import wraps
from flask import render_template, make_response
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity

def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            verify_jwt_in_request()
            current_user = get_jwt_identity()
            print(f"Current user: {current_user}")  # Debug print
        except Exception as e:
            print(f"Token verification error: {str(e)}")  # Debug print
            error_msg = "You must be Logged In to access this page"
            resp = make_response(render_template('login.html', error=error_msg))
            return resp
        return f(*args, **kwargs)
    return decorated_function
