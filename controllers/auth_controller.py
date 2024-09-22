'''
Here all the routes related to login/ signup will come'''

from services.auth_service import generate_tokens
from models.model import DatabaseConnection
from flask import render_template, request, make_response
from flask import Blueprint, render_template

auth_routes = Blueprint('auth_routes', __name__)

db_conn = DatabaseConnection()
db = db_conn.get_db()

@auth_routes.route('/login', methods = ["GET", "POST"])
def login_page():
    if request.method == "POST":
        usern = request.form.get('user')
        passw = request.form.get('pass')

        collection = db['users']
        try:
            data = collection.find_one({"name": usern})
        except Exception as e:
            print(f"Error retrieving data: {e}")  # Catch any errors while retrieving data
        
        if (data) is not None:
            if (data['password'] != passw):
                error_message = "Wrong Credentials"
                return render_template('login.html', error=error_message)
            else:
                tokens = generate_tokens(usern)
                resp = make_response(render_template('index.html'))
                resp.set_cookie('access_token_cookie', tokens.get('access_token'), httponly=True, samesite='Lax')
                resp.set_cookie('refresh_token_cookie', tokens.get('refresh_token'), httponly=True, samesite='Lax')
                return resp
        else:
            error_message = "Wrong Credentials"
            return render_template('login.html', error=error_message)
        
    return render_template('login.html')

@auth_routes.route('/signup', methods = ["GET", "POST"])
def signup_page():
    if request.method == "POST":
        usern = request.form.get('user')
        passw = request.form.get('pass')
        email = request.form.get('email')

        form_data = {'name':usern, 'password':passw, 'email':email}
        
        try:
            find_user = db['users'].find_one({"name":usern})
            find_email = db['users'].find_one({"email":email})
            if (find_user) is not None:
                error_msg = "Username Already Exists!"
                return render_template('signup.html', error=error_msg)
            if (find_email) is not None:
                error_msg = "Account Already Exists with this Email!"
                return render_template('signup.html', error=error_msg)
            
            if all([usern, passw, email]):
                inserted_id = db_conn.insert_document(form_data)
                print(f"Document inserted with ID: {inserted_id}")
                login_msg = "Account Registered Successfully"
                return render_template('login.html', login=login_msg)

        except ValueError as e:
            print(f"Validation Error: {e}")
    
    return render_template('signup.html')