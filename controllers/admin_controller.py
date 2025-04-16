import bcrypt
from models.model import DatabaseConnection
from services.auth_service import generate_tokens
from middlewares.admin_middleware import admin_required
from flask import Blueprint, request, render_template,make_response

admin_routes = Blueprint('admin_routes', __name__)

db_conn = DatabaseConnection()
db = db_conn.get_db()

@admin_routes.route('/admin', methods = ["GET", "POST"])
def login_page():
    if request.method == "POST":
        usern = request.form.get('user')
        passw = request.form.get('pass')

        collection = db['users']
        try:
            data = collection.find_one({"name": usern})
        except Exception as e:
            print(f"Error retrieving data: {e}")
        
        if (data) is not None:
            if not bcrypt.checkpw(passw.encode('utf-8'), data['password']):
                error_msg = "Wrong Credentials"
                return render_template('admin_login.html', error=error_msg)
            else:
                if (data['role'] == 0):
                    error_msg = "You are not an Admin"
                    return render_template('admin_login.html', error=error_msg)
                else:
                    tokens = generate_tokens(usern)
                    resp = make_response(render_template('admin_home.html', user=usern))
                    resp.set_cookie('access_token', tokens.get('access_token'), httponly=True)
                    resp.set_cookie('refresh_token', tokens.get('refresh_token'), httponly=True)
                    return resp
        else:
            error_msg = "Wrong Credentials"
            return render_template('admin_login.html', error=error_msg)
        
    return render_template('admin_login.html')

@admin_routes.route('/admin/assign_role', methods=['POST'])
@admin_required
def assign_role():
    if request.method == 'POST':
        username = request.form['username']
        role = request.form['role']
        if (role == 1):
            return render_template('admin_home.html', error="User is already an Admin")
        db['users'].update_one({'username': username}, {'$set': {'role': role}})
        return 'Role updated', 200
    
    return render_template('admin_home.html')