import traceback
from main import generate_frames
from conn.conn import DatabaseConnection
from flask import Flask,render_template,Response, request

db_conn = DatabaseConnection()
db = db_conn.get_db()

app=Flask(__name__)

@app.route('/')
def index():
    return render_template('login.html')    

@app.route('/video')
def video():
    return render_template('video.html')    

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/login', methods = ["POST"])
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
                return "Wrong Credentials"
            else:
                return render_template('video.html')
        else:
            return "Wrong Credentials"
        
    return render_template('login.html')

@app.route('/signup', methods = ["POST"])
def signup_page():
    if request.method == "POST":
        usern = request.form.get('user')
        passw = request.form.get('pass')
        email = request.form.get('email')

        form_data = {'name':usern, 'password':passw, 'email':email}
        
        try:
            inserted_id = db_conn.insert_document(form_data)
            print(f"Document inserted with ID: {inserted_id}")
            return render_template('login.html')
        except ValueError as e:
            print(f"Validation Error: {e}")
    return render_template('signup.html')

@app.errorhandler(500)
def internal_error(error):
    print(traceback.format_exc())  # Print the full error traceback
    return "An internal error occurred.", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)