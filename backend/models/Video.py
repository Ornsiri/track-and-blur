from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column,String,Integer,Date,DateTime
from sqlalchemy.dialects.postgresql import JSON
from datetime import datetime
from app import db

class Video(db.Model):
    __tablename__ = "videos"
    vid_id = db.Column(Integer, primary_key=True, nullable=False)
    vid_filename = db.Column(String, nullable=False)
    vid_datetime = db.Column(DateTime, nullable=False)
    vid_post_by = db.Column(String,nullable=False)
    user_id = db.Column(Integer,nullable=False)

    def __init__(self,vid_filename,vid_post_by,user_id):
        self.vid_id
        self.vid_filename = vid_filename
        self.vid_datetime = datetime.now()
        self.vid_post_by = vid_post_by
        self.user_id = user_id
        
        
    
    

        