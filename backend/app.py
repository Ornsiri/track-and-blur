import os
import psycopg2
import psycopg2.extras
import urllib.request
import time
import json
from datetime import datetime, timedelta

from vid2blur import blurvid
from flask import Flask, jsonify, render_template, request,flash,url_for, session, redirect, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash
from werkzeug.utils import secure_filename


app = Flask(__name__)
env_config = os.getenv("APP_SETTINGS", "config.DevelopmentConfig")
app.config.from_object(env_config)
app.permanent_session_lifetime = timedelta(hours=1)
db=SQLAlchemy(app)

from models.User import User
from models.Video import Video
from models.Request import Request

UPLOAD_USER_IMG = 'static/assets/upload_usr_img'
UPLOAD_VIDEO_BLUR = 'static/assets/upload_videos/blur/'
UPLOAD_VIDEO_UNBLUR = 'static/assets/upload_videos/unblur/'
ALLOWED_IMG_EXTENSIONS = set(['jpeg','jpg','png'])
ALLOWED_VIDEO_EXTENSIONS = set(['mp4','mov'])

app.config['UPLOAD_USER_IMG'] = UPLOAD_USER_IMG
app.config['UPLOAD_VIDEO_UNBLUR'] = UPLOAD_VIDEO_UNBLUR
app.config['UPLOAD_VIDEO_BLUR'] = UPLOAD_VIDEO_BLUR

connection = psycopg2.connect(dbname=app.config['DB_NAME'], user=app.config['DB_USERNAME'], 
                password=app.config['DB_PASSWORD'], host=app.config['DB_HOST'] ) 
print(app.config["SECRET_KEY"])
def allowed_img_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_IMG_EXTENSIONS

def allowed_video_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_VIDEO_EXTENSIONS

# @app.route('/')
# def index():
#     print(app.config)
#     secret_key = app.config.get("SECRET_KEY")
#     return f"The configured secret key is {secret_key}."


@app.route('/')
def landing():
    return render_template('html/landing.html')

@app.route('/import-video-successfully/<filename>', methods=['POST','GET'])
def upload_video_successfully(filename):
    print(session['user_img_file'])
    # session['user_img_file']
    # if session['user_img_file']:
    #     filename = secure_filename(session['user_img_file'])
    #     img_filepath = os.path.join(app.config['UPLOAD_USER_IMG'],filename)
    inpath = os.path.join(app.config['UPLOAD_VIDEO_UNBLUR'], filename)
    outpath = app.config['UPLOAD_VIDEO_BLUR']
    blurvid(inpath,outpath,filename)
    flash("Render is completed","success")
    time.sleep(5)
    return redirect(url_for('upload_video'))


@app.route('/import-video')
def upload_video():
    if 'loggedin' in session:
        return render_template('html/import-video.html', session = session)
    return redirect(url_for('signin'))

@app.route('/import-video', methods=['POST','GET'])
def upload_video_file():
    if 'loggedin' in session:
        if request.method == 'POST' and 'videofile' in request.files:
            _videofile  = request.files['videofile']
            
            if _videofile.filename and allowed_video_file(_videofile.filename): 
                filename = secure_filename(_videofile.filename)
            
            # return render_template('html/import-successfully.html',session = session, filename=filename)
            
            cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute('SELECT vid_filename FROM videos WHERE vid_filename = %s', (filename,))
            exist_vid = cursor.fetchone()
            if exist_vid:
                flash('This video is already existed', 'danger')
                return redirect(url_for('upload_video'))
            else :
                
                video = Video(str(filename),session['user_username'],session['user_id'])
                db.session.add(video)
                db.session.commit()
                video_unblur_path = os.path.join(app.config['UPLOAD_VIDEO_UNBLUR'], filename)
                _videofile.save(video_unblur_path)
                return render_template('html/import-successfully.html', filename = filename, session = session)

                # return redirect(url_for('upload_video_successfully',filename = filename))
            
        return redirect(url_for('upload_video'))
    return redirect(url_for('signin'))

@app.route('/signin', methods=['POST','GET'])
def signin():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        _username  = request.form['username']
        _password = request.form['password']

        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute('SELECT * FROM users WHERE user_username = %s', (_username,))
        user = cursor.fetchone()
        print(user)

        if user:
            if check_password_hash(user['user_password'],_password):
                session.permanant_session_lifetime = True
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
                    session['user_type'] = user['user_type']
                    session['user_img_file'] = user['user_img_file']
                    if session['user_img_file']:
                        filename = secure_filename(session['user_img_file'])
                        img_filepath = os.path.join(app.config['UPLOAD_USER_IMG'],filename)
                        session['user_img_file'] = img_filepath
                    print(img_filepath)
                    # print(session)
                    return redirect(url_for('upload_video'))
                
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
                    session['user_type'] = user['user_type']
                    session['user_img_file'] = user['user_img_file']
                    if session['user_img_file']:
                        filename = secure_filename(session['user_img_file'])
                        img_filepath = os.path.join(app.config['UPLOAD_USER_IMG'],filename)
                        session['user_img_file'] = img_filepath
                    # print(img_filepath)
                    # print(session['user_img_file'])

                    return redirect(url_for('upload_video'))
            else:
                flash("Invalid username or password","danger")
        else:
            flash("Invalid username or password","danger")
    return render_template('html/signin.html')

@app.route('/signup', methods=['POST','GET'])
def signup():
    if 'loggedin' in session:
        if request.method == 'POST' and \
        'fname' in request.form and \
        'lname' in request.form and \
        'email' in request.form and \
        'password' in request.form and \
        'tel' in request.form and \
        'dob' in request.form and \
        'user_type' in request.form and \
        'user_register_img' in request.files:
            _fname = request.form['fname']
            _lname = request.form['lname']
            _email = request.form['email']
            _password = request.form['password']
            _password = generate_password_hash(_password) 
            _tel = request.form['tel']
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
                    _user_img_file.filename = "user.png"
                
                if str(_user_type)=="1":
                    _user_type = "Admin"
                    user = User(_fname,_lname,_email,_password,_tel,_dob,_user_img_file.filename,_user_type)
                    db.session.add(user)
                    db.session.commit()
                    flash('A new user successfully added', 'success')
                    return render_template('html/signup.html', session=session)

                elif str(_user_type) == "2":
                    _user_type = "User"
                    user = User(_fname,_lname,_email,_password,_tel,_dob,_user_img_file.filename,_user_type)
                    db.session.add(user)
                    db.session.commit()
                    flash('A new user successfully added', 'success')
                    return render_template('html/signup.html', session=session)
        # return render_template('html/signup.html', session=session)
        return render_template('html/signup.html', session=session)
    return redirect(url_for('signin'))

@app.route('/search-video')
def search():
    if 'loggedin' in session:
        return render_template('html/search.html', session=session)
    return redirect(url_for('signin'))

@app.route('/search-video',methods=['POST','GET'] )
def get_search_video():
    if 'loggedin' in session:
        if request.method == 'POST' and \
        'startdate' in request.form and \
        'enddate' in request.form :
            # _camerano = request.form['camerano']
            _startdate = request.form['startdate']
            _enddate = request.form['enddate']
            _starttime = request.form['starttime']
            _endtime = request.form['endtime']
            videos = []
            try: 

                cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
                cursor.execute("""
                    SELECT *
                    FROM videos
                    WHERE vid_datetime BETWEEN %s AND %s
                    AND (vid_id NOT IN (
                        SELECT vid_id
                        FROM requests
                        WHERE user_id = %s
                        AND (status = 'Approved' OR status = 'Processing')
                    ) AND (videos.vid_post_by != (
                        SELECT user_username
                        FROM users
                        WHERE user_id = %s
                    )))
                    """,(_startdate+" "+_starttime,_enddate +" "+_endtime, session['user_id'],session['user_id']))


                # cursor.execute("""
                # select * from videos where vid_datetime 
                # between %s and %s
                # and (vid_id != (
                #     select vid_id from requests where user_id = %s 
                #     and (status = 'Approved' or status = 'Processing')
                # )
                # and (videos.vid_post_by != (
                #     select user_username from users where user_id = %s) 
                # ))""",
                # (_startdate+" "+_starttime,_enddate +" "+_endtime, session['user_id'],session['user_id']))

                videos = cursor.fetchall()
                connection.commit()
                
                if 'videos' in session:
                    session.pop('videos')

                if len(videos) > 0:
                    for video in videos:
                        print(video)
                        # add date month year to list
                        video.append(datetime.strftime(video[2],'%d %b %Y'))
                        # add time to list
                        t = datetime.strftime(video[2],'%H:%M')
                        if 0 <= int(t[:2]) < 12:
                            t = "AM"
                        else :
                            t = "PM"
                        day_upload = video[2]
                        video.append(datetime.strftime(video[2],'%H:%M') + " " + t)
                        # add day active to list
                        today = datetime.now()
                        dt = today - day_upload
                        dt = str(dt)
                        print(dt)
                        print(today)
                        if ',' in dt:
                            dt = dt.split(",")
                            d = dt[0]
                            h,m,s = dt[1].split(":")
                            if int(d[0]) < 1:
                                if int(h)==0 and int(m) == 0 and float(s) < 60: 
                                    s = "Just now"
                                    video.append(s)
                                elif int(h)==0 and int(m)  == 1:
                                    m = m + " minute ago"
                                    video.append(m)
                                elif int(h)==0 and int(m) > 1:
                                    m = m + " minutes ago"
                                    video.append(m)
                                elif int(h) == 1:
                                    h  = h + " hour ago"
                                    video.append(h)
                                elif int(h) > 1:
                                    h  = h + " hours ago"
                                    video.append(h)
                            elif int(d[0]) == 1:
                                d = d[0] + " day ago"
                                video.append(d)
                            else:
                                d = d + " ago"
                                video.append(d)
                        else :
                            h,m,s = dt.split(":")
                            if int(h)==0 and int(m) == 0 and float(s) < 60: 
                                s = "Just now"
                                video.append(s)
                            elif int(h)==0 and int(m)  == 1:
                                m = m + " minute ago"
                                video.append(m)
                            elif int(h)==0 and int(m) > 1:
                                m = m + " minutes ago"
                                video.append(m)
                            elif int(h) == 1:
                                h  = h + " hour ago"
                                video.append(h)
                            elif int(h) > 1:
                                h  = h + " hours ago"
                                video.append(h)
                        print(video)
                    session['videos'] = videos
                    session['blur_path'] = UPLOAD_VIDEO_BLUR
                    # print(session['blur_path'])
                else :
                    flash("No video result","danger")
            except psycopg2.Error as e:
                print("Select query error:", e)
                connection.rollback()

        return render_template('html/search.html', videos = videos,session=session)
    return redirect(url_for('signin'))

@app.route('/search-video/request-unblur/<int:vid_id>',methods=['POST','GET'] )
def request_unblur(vid_id):
    if 'loggedin' in session:
        try:
            user_id = session['user_id']
            request = Request(vid_id,user_id)
            db.session.add(request)
            db.session.commit()
            flash("Your request was sent","success")
        except:
            flash("Error, Please try again later","danger")
        return redirect(url_for('search'))
    return redirect(url_for('signin'))

@app.route('/uploaded',methods=['POST','GET'])
def request_upload():
    if 'loggedin' in session:
        try:
            user_id = session['user_id']
            cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute('SELECT * FROM videos WHERE user_id = %s',(user_id,))
            uploaded_videos = cursor.fetchall()
            session['unblur_path'] = UPLOAD_VIDEO_UNBLUR
            session['uploaded_videos'] = uploaded_videos
            for video in uploaded_videos:
                # add date month year to list
                video.append(datetime.strftime(video[2],'%d %b %Y'))
                # add time to list
                t = datetime.strftime(video[2],'%H:%M')
                if 0 <= int(t[:2]) < 12:
                    t = "AM"
                else :
                    t = "PM"
                day_upload = video[2]
                video.append(datetime.strftime(video[2],'%H:%M') + " " + t)
                # add day active to list
                today = datetime.now()
                dt = today - day_upload
                dt = str(dt)
                if ',' in dt:
                    dt = dt.split(",")
                    d = dt[0]
                    h,m,s = dt[1].split(":")
                    if int(d[0]) < 1:
                        if int(h)==0 and int(m) == 0 and float(s) < 60: 
                            s = "Just now"
                            video.append(s)
                        elif int(h)==0 and int(m)  == 1:
                            m = m + " minute ago"
                            video.append(m)
                        elif int(h)==0 and int(m) > 1:
                            m = m + " minutes ago"
                            video.append(m)
                        elif int(h) == 1:
                            h  = h + " hour ago"
                            video.append(h)
                        elif int(h) > 1:
                            h  = h + " hours ago"
                            video.append(h)
                    elif int(d[0]) == 1:
                        d = d[0] + " day ago"
                        video.append(d)
                    else:
                        d = d + " ago"
                        video.append(d)
                else :
                    h,m,s = dt.split(":")
                    if int(h)==0 and int(m) == 0 and float(s) < 60: 
                        s = "Just now"
                        video.append(s)
                    elif int(h)==0 and int(m)  == 1:
                        m = m + " minute ago"
                        video.append(m)
                    elif int(h)==0 and int(m) > 1:
                        m = m + " minutes ago"
                        video.append(m)
                    elif int(h) == 1:
                        h  = h + " hour ago"
                        video.append(h)
                    elif int(h) > 1:
                        h  = h + " hours ago"
                        video.append(h)
                # print(video)
            return render_template('html/request-upload.html', session = session,uploaded_videos=uploaded_videos)
        except psycopg2.Error as e:
            print("Uploaded query error:", e)
        return render_template('html/request-upload.html', session = session)
    return redirect(url_for('signin'))

@app.route('/approved')
def request_approve():
    if 'loggedin' in session:
        try:
            user_id = session['user_id']
            cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute('SELECT * FROM requests JOIN videos ON videos.vid_id = requests.vid_id WHERE requests.user_id = %s AND (status = %s OR status = %s)',(user_id,'Approved','Rejected',))
            approved_videos = []
            reject_videos = []
            videos = cursor.fetchall()
            session['unblur_path'] = UPLOAD_VIDEO_UNBLUR
            # session['approved_videos'] = approved_videos
            for video in videos:
                # add date month year to list
                video.append(datetime.strftime(video[3],'%d %b %Y'))
                # add time to list
                t = datetime.strftime(video[3],'%H:%M')
                if 0 <= int(t[:2]) < 12:
                    t = "AM"
                else :
                    t = "PM"
                day_upload = video[3]
                video.append(datetime.strftime(video[3],'%H:%M') + " " + t)
                # add day active to list
                today = datetime.now()
                dt = today - day_upload
                dt = str(dt)
                if ',' in dt:
                    dt = dt.split(",")
                    d = dt[0]
                    h,m,s = dt[1].split(":")
                    if int(d[0]) < 1:
                        if int(h)==0 and int(m) == 0 and float(s) < 60: 
                            s = "Just now"
                            video.append(s)
                        elif int(h)==0 and int(m)  == 1:
                            m = m + " minute ago"
                            video.append(m)
                        elif int(h)==0 and int(m) > 1:
                            m = m + " minutes ago"
                            video.append(m)
                        elif int(h) == 1:
                            h  = h + " hour ago"
                            video.append(h)
                        elif int(h) > 1:
                            h  = h + " hours ago"
                            video.append(h)
                    elif int(d[0]) == 1:
                        d = d[0] + " day ago"
                        video.append(d)
                    else:
                        d = d + " ago"
                        video.append(d)
                else :
                    h,m,s = dt.split(":")
                    if int(h)==0 and int(m) == 0 and float(s) < 60: 
                        s = "Just now"
                        video.append(s)
                    elif int(h)==0 and int(m)  == 1:
                        m = m + " minute ago"
                        video.append(m)
                    elif int(h)==0 and int(m) > 1:
                        m = m + " minutes ago"
                        video.append(m)
                    elif int(h) == 1:
                        h  = h + " hour ago"
                        video.append(h)
                    elif int(h) > 1:
                        h  = h + " hours ago"
                        video.append(h)
                # separate status
                if video[4] == "Approved" :
                    approved_videos.append(video)
                elif video[4] == "Rejected" :
                    reject_videos.append(video)
                print("Reject: ",reject_videos)
                print("Approved: ",approved_videos)

            return render_template('html/request-approve.html', session = session,approved_videos=approved_videos,reject_videos= reject_videos)
        except psycopg2.Error as e:
            print("Approved query error:", e)
        return render_template('html/request-approve.html', session = session)
    return redirect(url_for('signin'))


@app.route('/waiting')
def request_waiting():
    if 'loggedin' in session:
        try:
            user_id = session['user_id']
            cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute('SELECT * FROM requests JOIN videos ON videos.vid_id = requests.vid_id WHERE requests.user_id = %s AND status = %s',(user_id,'Processing',))
            processing_videos = cursor.fetchall()
            session['unblur_path'] = UPLOAD_VIDEO_UNBLUR
            session['blur_path'] = UPLOAD_VIDEO_BLUR
            session['processing_videos'] = processing_videos
            for video in processing_videos:
                # add date month year to list
                video.append(datetime.strftime(video[3],'%d %b %Y'))
                # add time to list
                t = datetime.strftime(video[3],'%H:%M')
                if 0 <= int(t[:2]) < 12:
                    t = "AM"
                else :
                    t = "PM"
                day_upload = video[3]
                video.append(datetime.strftime(video[3],'%H:%M') + " " + t)
                # add day active to list
                today = datetime.now()
                dt = today - day_upload
                dt = str(dt)
                if ',' in dt:
                    dt = dt.split(",")
                    d = dt[0]
                    h,m,s = dt[1].split(":")
                    if int(d[0]) < 1:
                        if int(h)==0 and int(m) == 0 and float(s) < 60: 
                            s = "Just now"
                            video.append(s)
                        elif int(h)==0 and int(m)  == 1:
                            m = m + " minute ago"
                            video.append(m)
                        elif int(h)==0 and int(m) > 1:
                            m = m + " minutes ago"
                            video.append(m)
                        elif int(h) == 1:
                            h  = h + " hour ago"
                            video.append(h)
                        elif int(h) > 1:
                            h  = h + " hours ago"
                            video.append(h)
                    elif int(d[0]) == 1:
                        d = d[0] + " day ago"
                        video.append(d)
                    else:
                        d = d + " ago"
                        video.append(d)
                else :
                    h,m,s = dt[0].split(":")
                    if int(h)==0 and int(m) == 0 and float(s) < 60: 
                        s = "Just now"
                        video.append(s)
                    elif int(h)==0 and int(m)  == 1:
                        m = m + " minute ago"
                        video.append(m)
                    elif int(h)==0 and int(m) > 1:
                        m = m + " minutes ago"
                        video.append(m)
                    elif int(h) == 1:
                        h  = h + " hour ago"
                        video.append(h)
                    elif int(h) > 1:
                        h  = h + " hours ago"
                        video.append(h)
                print(video)
            return render_template('html/request-waiting.html', session = session,processing_videos=processing_videos)
        except :
            print("Waiting query is error")
        return render_template('html/request-waiting.html', session = session)
    return redirect(url_for('signin'))

@app.route('/requested')
def admin_request():
    if 'loggedin' in session:
        try:
            cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
            # cursor.execute('SELECT * FROM requests JOIN videos ON videos.vid_id = requests.vid_id WHERE status = %s',('Processing',))
            cursor.execute("""
                SELECT requests.request_id,
                requests.vid_id,
                requests.user_id,
                requests.date_requested,
                requests.status,
                requests.checked_by_admin_id,
                videos.vid_id,
                videos.vid_filename,
                videos.vid_datetime,
                videos.vid_post_by,
                videos.user_id,
                users.user_id,
                users.user_username
                FROM requests 
                JOIN videos ON videos.vid_id = requests.vid_id 
                JOIN users ON users.user_id = requests.user_id
                WHERE status = %s
            """,('Processing',))
            processing_videos = cursor.fetchall()
            session['blur_path'] = UPLOAD_VIDEO_BLUR
            session['processing_videos'] = processing_videos
            for video in processing_videos:
                # add date month year to list
                video.append(datetime.strftime(video[3],'%d %b %Y'))
                # add time to list
                t = datetime.strftime(video[3],'%H:%M')
                if 0 <= int(t[:2]) < 12:
                    t = "AM"
                else :
                    t = "PM"
                day_upload = video[3]
                video.append(datetime.strftime(video[3],'%H:%M') + " " + t)
                # add day active to list
                today = datetime.now()
                dt = today - day_upload
                dt = str(dt)
                if ',' in dt:
                    dt = dt.split(",")
                    d = dt[0]
                    h,m,s = dt[1].split(":")
                    if int(d[0]) < 1:
                        if int(h)==0 and int(m) == 0 and float(s) < 60: 
                            s = "Just now"
                            video.append(s)
                        elif int(h)==0 and int(m)  == 1:
                            m = m + " minute ago"
                            video.append(m)
                        elif int(h)==0 and int(m) > 1:
                            m = m + " minutes ago"
                            video.append(m)
                        elif int(h) == 1:
                            h  = h + " hour ago"
                            video.append(h)
                        elif int(h) > 1:
                            h  = h + " hours ago"
                            video.append(h)
                    elif int(d[0]) == 1:
                        d = d[0] + " day ago"
                        video.append(d)
                    else:
                        d = d + " ago"
                        video.append(d)
                else :
                    h,m,s = dt.split(":")
                    if int(h)==0 and int(m) == 0 and float(s) < 60: 
                        s = "Just now"
                        video.append(s)
                    elif int(h)==0 and int(m)  == 1:
                        m = m + " minute ago"
                        video.append(m)
                    elif int(h)==0 and int(m) > 1:
                        m = m + " minutes ago"
                        video.append(m)
                    elif int(h) == 1:
                        h  = h + " hour ago"
                        video.append(h)
                    elif int(h) > 1:
                        h  = h + " hours ago"
                        video.append(h)
                print(video)
            return render_template('html/requested.html', session = session,processing_videos=processing_videos)
        except psycopg2.Error as e:
            print("Select query error:", e)
        return render_template('html/requested.html', session=session)
    return redirect(url_for('signin'))


@app.route('/permission')
def admin_permission():
    if 'loggedin' in session:
        return render_template('html/permission.html', session=session)
    return redirect(url_for('signin'))


@app.route('/approve-confirmed/<int:vid_id>', methods=['POST','GET'])
def confirm_approve(vid_id):
    if 'loggedin' in session:
        try:
            user_id = session['user_id']
            cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute('UPDATE requests SET status = %s, checked_by_admin_id = %s WHERE vid_id = %s',
                           ('Approved', user_id, vid_id))
            connection.commit()
        except psycopg2.Error as e:
            print("Update query error:", e)
        
        return redirect(url_for('admin_request'))
    return redirect(url_for('signin'))

@app.route('/reject-confirmed/<int:vid_id>/<int:user_id>', methods=['POST', 'GET'])
def confirm_reject(vid_id,user_id):
    if 'loggedin' in session:
        try:
            cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute('UPDATE requests SET status = %s, checked_by_admin_id = %s WHERE vid_id = %s',
                           ('Rejected', session['user_id'], vid_id))
            # cursor.execute('DELETE FROM requests WHERE vid_id = %s AND user_id = %s AND status = %s RETURNING * ', (vid_id, user_id,'Processing'))
            connection.commit()
        except psycopg2.Error as e:
            print("Delete query error:", e)

        return redirect(url_for('admin_request'))
    return redirect(url_for('signin'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('signin'))



if __name__ == '__main__':
    
    app.run(debug = True)
