from flask import Flask, jsonify, render_template, request,flash,url_for, session, redirect
import psycopg2
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column,String,Integer,Date,DateTime
from werkzeug.security import generate_password_hash,check_password_hash
from werkzeug.utils import secure_filename
import os
from datetime import datetime
import uuid
import urllib.request

app = Flask(__name__)

UPLOAD_USER_IMG_FOLDER = 'static/assets/upload_usr_imgs'
UPLOAD_VIDEO_FOLDER = 'static/assets/upload_videos'
app.config['UPLOAD_USER_IMG_FOLDER'] = UPLOAD_USER_IMG_FOLDER
app.config['UPLOAD_VIDEO_FOLDER'] = UPLOAD_VIDEO_FOLDER

ALLOWED_IMG_EXTENSIONS = set(['jpeg','jpg','png'])
ALLOWED_VIDEO_EXTENSIONS = set([])

# DB_HOST = "localhost"
# DB_NAME = "track_and_blur"
# DB_USER = "postgres"
# DB_PASS = "admin"

# connection = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost/track_and_blur'
db=SQLAlchemy(app)

class Admin(db.Model):
    __tablename__ = "admin"
    admin_uuid = db.Column(String,primary_key = True)
    admin_fname = db.Column(String)
    admin_lname = db.Column(String) 
    admin_email = db.Column(String)
    admin_password = db.Column(String)
    admin_tel = db.Column(String)
    admin_dob = db.Column(Date)
    admin_img_filename = db.Column(String)
    admin_username = db.Column(String)
    admin_regis_on = db.Column(DateTime)


    def __init__(self,fname,lname,email,password,tel,dob,user_register_img):
        self.admin_uuid = uuid.uuid4()
        self.admin_fname=fname
        self.admin_lname=lname
        self.admin_email=email
        self.admin_password=password
        self.admin_tel=tel
        self.admin_dob=dob
        self.admin_img_filename = user_register_img
        self.admin_username = self.admin_fname + self.admin_tel[5:9]
        self.admin_regis_on = datetime.now()

    # pass

def allowed_img_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_IMG_EXTENSIONS

def allowed_video_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_VIDEO_EXTENSIONS

@app.route('/landing')
def landing():
    return render_template('html/landing.html')

@app.route('/home')
def main():
    return render_template('html/import-video.html')

@app.route('/import-video')
def upload():
    return render_template('html/import-video.html')

@app.route('/signin', methods=['POST','GET'])
def signin():
    # cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    # if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
    #     _username = request.form['username']
    #     _password = request.form['password']
    #     _password = generate_password_hash(_password) 
    #     # print(generate_password_hash(password))   
    #     # _json = request.json
    #     # _username = _json['username']
    #     # _password = _json['password']
    #     if _username and _password:
    #         sql = "SELECT * FROM users WHERE username=%s"
    #         where = (_username,)

    #         cursor.execute(sql,where)
    #         row = cursor.fetchone()
    #         username = row['username']
    #         password = row['password']
    #         print(username)
    #         print(password)

    #         # if _username == username and _password == password:
    #         #     return redirect(url_for('upload'))


    return render_template('html/signin.html')

@app.route('/signup', methods=['GET','POST'])
def signup():
    
    if request.method == 'POST' and \
        'fname' in request.form and \
        'lname' in request.form and \
        'email' in request.form and \
        'password' in request.form and \
        'tel' in request.form and \
        'dob' in request.form and \
        'department' in request.form and \
        'user_type' in request.form and \
        'user_register_img' in request.form:
        
        _fname = request.form['fname']
        _lname = request.form['lname']
        _email = request.form['email']
        _password = request.form['password']
        _password = generate_password_hash(_password) 
        _tel = request.form['tel']
        _dob = request.form['dob']
        _user_type = request.form['user_type']
        _user_register_img = request.form['user_register_img']

        if str(_user_type)=="1":
            admin = Admin(_fname,_lname,_email,_password,_tel,_dob,_user_register_img)
            db.session.add(admin)
            db.session.commit()
        elif str(_user_type) == "2":
            pass
        elif str(_user_type) == "3":
            pass



        



        flash('A new user successfully added')

        return render_template('/html/import-video.html')

    _regis_on = datetime.now()
    print(_regis_on)


        




    return render_template('html/signup.html')

@app.route('/search-video')
def search():
    return render_template('html/search.html')

@app.route('/permission')
def permission():
    return render_template('html/permission.html')

if __name__ == '__main__':
    

    app.run(debug = True)
