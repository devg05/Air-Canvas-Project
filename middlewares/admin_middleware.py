from functools import wraps
from models.model import DatabaseConnection
from flask import render_template, make_response, request
from middlewares.auth_middleware import verify_jwt_in_request, get_jwt_identity

db_conn = DatabaseConnection()
db = db_conn.get_db()

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            result, status_code = verify_jwt_in_request()  # Call the custom function
            if status_code != 200:
                raise Exception(result)
            current_user = get_jwt_identity(result)
            user = db['users'].find_one({'username': current_user})

            if user['role'] == 0:
                error_msg = "You must be an Admin to access this page"
                resp = make_response(render_template('login.html', error=error_msg))
                return
            
            elif user['role'] == 1 :
                return render_template('admin.html')
            print(f"Current user: {current_user}")  # Debug print

        except Exception as e:
            print(f"Token verification error: {str(e)}")  # Debug print
            error_msg = "You must be Logged In to access this page"
            resp = make_response(render_template('login.html', error=error_msg))
            return resp
        return f(*args, **kwargs)
    return decorated_function