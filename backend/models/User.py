from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column,String,Integer,Date,DateTime
from sqlalchemy.dialects.postgresql import JSON
from datetime import datetime
from app import db

class User(db.Model):
    __tablename__ = "users"
    user_id= db.Column(Integer,primary_key = True)
    user_fname = db.Column(String, nullable=False)
    user_lname = db.Column(String, nullable=False) 
    user_email = db.Column(String, nullable=False)
    user_password = db.Column(String, nullable=False)
    user_tel = db.Column(String, nullable=False)
    user_dob = db.Column(Date, nullable=False)
    user_department = db.Column(String,nullable=True)
    user_img_file = db.Column(String,nullable=True)
    user_username = db.Column(String, unique=True, nullable= False)
    user_type = db.Column(String, nullable=False)
    user_regis_on = db.Column(DateTime, nullable=False)


    def __init__(self,fname,lname,email,password,tel,dob,department,user_img_file,user_type):
        self.user_id 
        self.user_fname=fname
        self.user_lname=lname
        self.user_email=email
        self.user_password=password
        self.user_tel=tel
        self.user_dob=dob
        self.user_department = department
        self.user_img_file = user_img_file
        self.user_username = self.user_fname + self.user_tel[6:10]
        self.user_type = user_type
        self.user_regis_on = datetime.now()

