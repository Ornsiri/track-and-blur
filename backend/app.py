import os
import psycopg2
import psycopg2.extras
import urllib.request

from flask import Flask, jsonify, render_template, request,flash,url_for, session, redirect, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from werkzeug.security import generate_password_hash,check_password_hash
from werkzeug.utils import secure_filename


app = Flask(__name__)
env_config = os.getenv("APP_SETTINGS", "config.DevelopmentConfig")
app.config.from_object(env_config)
db=SQLAlchemy(app)

from models.User import User

UPLOAD_USER_IMG = 'static/assets/upload_usr_img'
ALLOWED_IMG_EXTENSIONS = set(['jpeg','jpg','png'])

app.config['UPLOAD_USER_IMG'] = UPLOAD_USER_IMG
# app.config['UPLOAD_VIDEO'] = UPLOAD_VIDEO

# ALLOWED_VIDEO_EXTENSIONS = set([])

# DB_HOST = "localhost"
# DB_NAME = "track_and_blur"
# DB_USER = "postgres"
# DB_PASS = "admin"

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost/track_and_blur'

connection = psycopg2.connect(dbname=app.config['DB_NAME'], user=app.config['DB_USERNAME'], 
                password=app.config['DB_PASSWORD'], host=app.config['DB_HOST'] ) 

def allowed_img_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_IMG_EXTENSIONS

# def allowed_video_file(filename):
#     return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_VIDEO_EXTENSIONS

# @app.route('/')
# def index():
#     print(app.config)
#     secret_key = app.config.get("SECRET_KEY")
#     return f"The configured secret key is {secret_key}."

@app.route('/')
def landing():
    return render_template('html/landing.html')

@app.route('/import-video')
def upload_video():
    if 'loggedin' in session:
        if session['user_img_file']:
            filename = secure_filename(session['user_img_file'])
            img_filepath = os.path.join(app.config['UPLOAD_USER_IMG'],filename)
        return render_template('html/import-video.html', filename=img_filepath)
    
    return redirect(url_for('signin'))

@app.route('/uploads/<filename>')
def get_file(filename):
    return redirect(url_for('static',filename='upload_usr_img/'+filename))
    # return send_from_directory(app.config['UPLOAD_USER_IMG'], filename)

@app.route('/signin', methods=['POST','GET'])
def signin():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        _username  = request.form['username']
        _password = request.form['password']

        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute('SELECT * FROM users WHERE user_username = %s', (_username,))
        user = cursor.fetchone()
        # print(user)
        if user:
            if check_password_hash(user['user_password'],_password):
                if user['user_type'] == "Admin":
                    session['loggedin'] = True
                    session['user_id'] = user['user_id']
                    session['user_username'] = user['user_username']
                    session['user_password'] = user['user_password']
                    session['user_email'] = user['user_email']
                    session['user_fname'] = user['user_fname']
                    session['user_lname'] = user['user_lname']
                    session['user_tel'] = user['user_tel']
                    session['user_dob'] = user['user_dob']
                    session['user_department'] = user['user_department']
                    session['user_type'] = user['user_type']
                    session['user_img_file'] = user['user_img_file']
                    if session['user_img_file']:
                        filename = secure_filename(session['user_img_file'])
                        img_filepath = os.path.join(app.config['UPLOAD_USER_IMG'],filename)
                    print(img_filepath)
                elif user['user_type'] == "User":
                    session['loggedin'] = True
                    session['user_id'] = user['user_id']
                    session['user_username'] = user['user_username']
                    session['user_password'] = user['user_password']
                    session['user_email'] = user['user_email']
                    session['user_fname'] = user['user_fname']
                    session['user_lname'] = user['user_lname']
                    session['user_tel'] = user['user_tel']
                    session['user_dob'] = user['user_dob']
                    session['user_department'] = user['user_department']
                    session['user_type'] = user['user_type']
                    session['user_img_file'] = user['user_img_file']
                    if session['user_img_file']:
                        filename = secure_filename(session['user_img_file'])
                        img_filepath = os.path.join(app.config['UPLOAD_USER_IMG'],filename)
                    print(img_filepath)
                
                return render_template('html/import-video.html', filename=img_filepath,user_type = user['user_type'])
            else:
                flash("Invalid username or password","danger")
        else:
            flash("Invalid username or password","danger")
    return render_template('html/signin.html')

@app.route('/signup', methods=['POST','GET'])
def signup():
    if 'loggedin' in session:
        if session['user_img_file']:
            filename = secure_filename(session['user_img_file'])
            img_filepath = os.path.join(app.config['UPLOAD_USER_IMG'],filename)
        if request.method == 'POST' and \
        'fname' in request.form and \
        'lname' in request.form and \
        'email' in request.form and \
        'password' in request.form and \
        'tel' in request.form and \
        'dob' in request.form and \
        'department' in request.form and \
        'user_type' in request.form and \
        'user_register_img' in request.files:
        
            _fname = request.form['fname']
            _lname = request.form['lname']
            _email = request.form['email']
            _password = request.form['password']
            _password = generate_password_hash(_password) 
            _tel = request.form['tel']
            _department = request.form['department']
            _dob = request.form['dob']
            _user_type = request.form['user_type']
            _user_img_file = request.files['user_register_img']

            cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute('SELECT user_fname, user_email FROM users WHERE user_email = %s', (_email,))
            exist_user = cursor.fetchone()
            if exist_user != None and exist_user[0] == _fname and exist_user[1] == _email:
                flash('This user is already existed', 'danger')
                return render_template('html/signup.html')
            else :
                if _user_img_file.filename and allowed_img_file(_user_img_file.filename):
                    filename = secure_filename(_user_img_file.filename)
                    _user_img_file.save(os.path.join(app.config['UPLOAD_USER_IMG'], filename))
                else :
                    _user_img_file = "user.png"
                
                if str(_user_type)=="1":
                    _user_type = "Admin"
                    user = User(_fname,_lname,_email,_password,_tel,_dob,_department,_user_img_file.filename,_user_type)
                    db.session.add(user)
                    db.session.commit()
                    flash('A new user successfully added', 'success')
                    return render_template('html/signup.html', filename=img_filepath)

                elif str(_user_type) == "2":
                    _user_type = "User"
                    user = User(_fname,_lname,_email,_password,_tel,_dob,_department,_user_img_file,_user_type)
                    db.session.add(user)
                    db.session.commit()
                    flash('A new user successfully added', 'success')
                    return render_template('html/signup.html', filename=img_filepath)
        return render_template('html/signup.html', filename=img_filepath)
    return render_template('html/signin.html')

@app.route('/search-video')
def search():
    if 'loggedin' in session:
        if session['user_img_file']:
            filename = secure_filename(session['user_img_file'])
            img_filepath = os.path.join(app.config['UPLOAD_USER_IMG'],filename)
        return render_template('html/search.html', filename=img_filepath)
    return render_template('html/signin.html')

@app.route('/permission')
def permission():
    if 'loggedin' in session:
        if session['user_img_file']:
            filename = secure_filename(session['user_img_file'])
            img_filepath = os.path.join(app.config['UPLOAD_USER_IMG'],filename)
        return render_template('html/permission.html', filename=img_filepath)
    return render_template('html/signin.html')

@app.route('/logout')
def logout():
    # session.pop('loggedin', None)
    # session.pop('user_id', None)
    # session.pop('user_username', None)
    # session.pop('user_password', None) 
    # session.pop('user_email', None)
    # session.pop('user_fname', None)
    # session.pop('user_lname',None)
    # session.pop('user_tel',None) 
    # session.pop('user_dob', None)
    # session.pop('user_department',None)
    # session.pop('user_type', None)
    # session.pop('user_img_file',None)
    session.clear()
    return redirect(url_for('signin'))



if __name__ == '__main__':
    
    app.run(debug = True)
