''' Code to check if user is autheticated or not'''

from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from functools import wraps

def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            verify_jwt_in_request()
            current_user = get_jwt_identity()
            print(f"Current user: {current_user}")  # Debug print
        except Exception as e:
            print(f"Token verification error: {str(e)}")  # Debug print
            return jsonify({'message': 'Token is invalid or missing'}), 401
        return f(*args, **kwargs)
    return decorated_function
