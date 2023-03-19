from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column,String,Integer,Date,DateTime
from sqlalchemy.dialects.postgresql import JSON
from datetime import datetime
from app import db

class Video(db.Model):
    __tablename__ = "videos"
    vid_id = db.Column(Integer, primary_key=True, nullable=False)
    vid_camera_no = db.Column(Integer, nullable=True)
    vid_datetime = db.Column(DateTime, nullable=False)
    vid_filename = db.Column(String, nullable=False)
    vid_type = db.Column(String, nullable=False)


    def __init__(self,vid_camera_no, vid_datetime, vid_filename, vid_type):
        self.vid_id
        self.vid_camera_no = vid_camera_no
        self.vid_datetime = vid_datetime
        self.vid_filename = vid_filename
        self.vid_type = vid_type
        
    
    

        