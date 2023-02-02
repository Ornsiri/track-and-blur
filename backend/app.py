from flask import Flask, render_template, request
import psycopg2
import psycopg2.extras
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

DB_HOST = "localhost"
DB_NAME = "track_and_blur"
DB_USER = "postgres"
DB_PASS = "admin"

connection = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)

@app.route('/')
def landing():
    return render_template('html/landing.html')

@app.route('/import-video')
def upload():
    return render_template('html/import-video.html')

@app.route('/signin', methods=['GET','POST'])
def signin():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']    
        print(username)
        print(password)    
    return render_template('html/signin.html')

@app.route('/signup', methods=['GET','POST'])
def signup():

    return render_template('html/signup.html')

@app.route('/search-video')
def search():
    return render_template('html/search.html')

@app.route('/permission')
def permission():
    return render_template('html/permission.html')

if __name__ == '__main__':
    app.run(debug = True)
