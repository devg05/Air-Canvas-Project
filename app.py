import os
from flask import Flask
from dotenv import load_dotenv
from datetime import timedelta
from flask_jwt_extended import JWTManager
from models.model import DatabaseConnection
from controllers.user_controller import user_routes
from controllers.auth_controller import auth_routes
from controllers.error_controller import error_handlers


db_conn = DatabaseConnection()
db = db_conn.get_db()

app=Flask(__name__)

load_dotenv()

app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES')))
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=int(os.getenv('JWT_REFRESH_TOKEN_EXPIRES')))

app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_SECURE'] = True  # Set to True if using HTTPS
app.config['JWT_COOKIE_CSRF_PROTECT'] = False 

jwt = JWTManager(app)

app.register_blueprint(user_routes)
app.register_blueprint(auth_routes)
app.register_blueprint(error_handlers)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)