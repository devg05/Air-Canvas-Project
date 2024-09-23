''' Code to check if user is autheticated or not'''

import os
import jwt
from functools import wraps
from flask import render_template, make_response, request

def verify_jwt_in_request():
    # Get tokens from cookies
    access_token = request.cookies.get('access_token')      # Name of your access token cookie
    refresh_token = request.cookies.get('refresh_token')    # Name of your refresh token cookie

    access_token_valid = False
    refresh_token_valid = False

    if access_token:
        try:
            jwt.decode(access_token, os.getenv('JWT_SECRET_KEY'), algorithms=["HS256"])     # Verify access token
            access_token_valid = True
        except jwt.ExpiredSignatureError:
            access_token_valid = False  # Token is expired
        except jwt.InvalidTokenError:
            access_token_valid = False  # Token is invalid

    if refresh_token:
        try:
            jwt.decode(refresh_token, os.getenv('JWT_SECRET_KEY'), algorithms=["HS256"])    # Verify refresh token
            refresh_token_valid = True
        except jwt.ExpiredSignatureError:
            refresh_token_valid = False
        except jwt.InvalidTokenError:
            refresh_token_valid = False

    if access_token_valid:
        return "Access token is valid", 200
    elif refresh_token_valid:
        return "Refresh token is valid", 200
    else:
        return "Both tokens are invalid or expired", 401
    
def get_jwt_identity(result):
    if result == "Access token is valid":
        username = jwt.decode(request.cookies.get('access_token'), os.getenv('JWT_SECRET_KEY'), algorithms=["HS256"])['sub']
    else:
        username = jwt.decode(request.cookies.get('refresh_token'), os.getenv('JWT_SECRET_KEY'), algorithms=["HS256"])['sub']
    return username
    
def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            result, status_code = verify_jwt_in_request()  # Call the custom function
            if status_code != 200:
                raise Exception(result)
            current_user = get_jwt_identity(result)
            print(f"Current user: {current_user}")  # Debug print
        except Exception as e:
            print(f"Token verification error: {str(e)}")  # Debug print
            error_msg = "You must be Logged In to access this page"
            resp = make_response(render_template('login.html', error=error_msg))
            return resp
        return f(*args, **kwargs)
    return decorated_function
