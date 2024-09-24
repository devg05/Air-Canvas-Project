'''
All the other routes are to be present here'''

# user_routes.py
from main import generate_frames
from middlewares.auth_middleware import token_required
from flask import Blueprint, render_template, Response, make_response
from middlewares.auth_middleware import verify_jwt_in_request, get_jwt_identity 

# Create a Blueprint
user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/')
def index():
    return render_template('login.html')

@user_routes.route('/home')
@token_required
def home():
    result, status_code = verify_jwt_in_request()  # Call the custom function
    if status_code != 200:
        raise Exception(result)
    current_user = get_jwt_identity(result)
    return render_template('home.html', user=current_user)

@user_routes.route('/video')
@token_required
def video():
    result, status_code = verify_jwt_in_request()  # Call the custom function
    if status_code != 200:
        raise Exception(result)
    current_user = get_jwt_identity(result)
    return render_template('video.html', user=current_user)

@user_routes.route('/video_feed')
@token_required
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@user_routes.route('/logout_page')
@token_required
def logout_page():
    logout_msg = "You have logged out successfully"
    resp = make_response(render_template('login.html', logout=logout_msg))
    resp.set_cookie('access_token', "", expires=0)
    resp.set_cookie('refresh_token', "", expires=0)
    return resp