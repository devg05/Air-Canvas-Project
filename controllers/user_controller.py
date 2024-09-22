'''
All the other routes are to be present here'''

# user_routes.py
from flask import Blueprint, render_template, Response
from main import generate_frames  # Import any necessary function from your project
from middlewares.auth_middleware import token_required

# Create a Blueprint
user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/')
def index():
    return render_template('login.html')

@user_routes.route('/video')
@token_required
def video():
    return render_template('video.html')

@user_routes.route('/video_feed')
@token_required
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
