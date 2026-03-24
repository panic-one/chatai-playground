from app.extensions import db

class Analyze(db.Model):
    __tablename__ = "analyses"

    analysis_id = db.Column(db.BigInteger, primary_key=True)
    message_id = db.Column(db.BigInteger, db.ForeignKey("messages.message_id"), nullable=False, index=True)
    analyzer_model = db.Column(db.String(30), nullable=False)
    category = db.Column(db.String(15), nullable=False)
    difficulty = db.Column(db.String(8), nullable=False)
    reason = db.Column(db.Text, nullable=False)
    total_score = db.Column(db.Integer, nullable=False)
    selected_provider = db.Column(db.String(10))
    selected_model = db.Column(db.String(30))
    is_fallback = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())

    message = db.relationship("Message", backref="analyses")