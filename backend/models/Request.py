from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column,String,Integer,Date,DateTime
from sqlalchemy.dialects.postgresql import JSON
from datetime import datetime
from app import db

class Request(db.Model):
    __tablename__ = "requests"
    request_id = db.Column(Integer, primary_key=True, nullable=False)
    vid_id = db.Column(Integer, nullable=False)
    user_id = db.Column(Integer, nullable=True)
    date_requested = db.Column(DateTime, nullable=False)
    status = db.Column(String,nullable=False)
    checked_by_admin_id = db.Column(Integer)

    def __init__(self,vid_id,user_id):
        self.request_id
        self.vid_id = vid_id
        self.user_id = user_id
        self.date_requested = datetime.now()
        self.status = "Processing"
        self.checked_by_admin_id

