from app.extensions import db
from datetime import datetime

class Message(db.Model):
    __tablename__ = "messages"

    message_id = db.Column(db.Integer, primary_key=True)
    thread_id = db.Column(db.Integer, db.ForeignKey("threads.thread_id"), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    firebase_uid = db.Column(db.String(128), index=True)
    model = db.Column(db.String(50))
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    message_index = db.Column(db.Integer, nullable=False)
