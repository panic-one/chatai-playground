from app.extensions import db

class Message(db.Model):
    __tablename__ = "messages"
    __table_args__ = (db.UniqueConstraint("thread_id", "message_index"),)

    message_id = db.Column(db.BigInteger, primary_key=True)
    thread_id = db.Column(db.BigInteger, db.ForeignKey("threads.thread_id"), nullable=False)
    role = db.Column(db.Integer, nullable=False)
    firebase_uid = db.Column(db.String(28), index=True)
    provider = db.Column(db.String(50), nullable=True)
    model = db.Column(db.String(50))
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    message_index = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False, default="completed")

    def to_dict(self):
        return {
            "message_id": self.message_id,
            "thread_id": self.thread_id,
            "role": self.role,
            "content": self.content,
            "provider": self.provider,
            "model": self.model,
            "firebase_uid": self.firebase_uid,
            "message_index": self.message_index,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "status": self.status,
        }