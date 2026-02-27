from app.extensions import db
from datetime import datetime

class Thread(db.Model):
    __tablename__ = "threads"

    thred_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    messages = db.relationship("Message", backref="thread", cascade="all, delete")