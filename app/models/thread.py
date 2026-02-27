from app.extensions import db
from datetime import datetime

class Thread(db.Model):
    __tablename__ = "threads"

    thread_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    firebase_uid = db.Column(db.String(128), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    messages = db.relationship("Message", backref="thread", cascade="all, delete")