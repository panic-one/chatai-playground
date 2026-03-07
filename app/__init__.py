from flask import Flask
from dotenv import load_dotenv
from .firebase import init_firebase
from datetime import timedelta
from .extensions import db, migrate
import os

def create_app():
    load_dotenv()

    app = Flask(__name__)

    env = os.environ.get("ENV", "development")
    is_prod = env == "production"

    if is_prod:
        secret = os.environ["SECRET_KEY"]
    else:
        secret = os.environ.get("SECRET_KEY", "dev-secret")
    
    app.config.update(
        SECRET_KEY=secret,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        SESSION_COOKIE_SECURE=is_prod,
        PERMANENT_SESSION_LIFETIME=timedelta(hours=8),
    )

    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        db_host = os.environ.get("DB_HOST", "db")
        db_user = os.environ.get("DB_USER", "postgres")
        db_password = os.environ.get("DB_PASSWORD", "postgres")
        db_name = os.environ.get("DB_NAME", "flask_db")
        db_url = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:5432/{db_name}"

    app.config.update(
        SQLALCHEMY_DATABASE_URI=db_url,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        from .models.thread import Thread
        from .models.message import Message

    init_firebase()

    @app.get("/health")
    def health():
        return "ok"

    from .auth import auth_bp
    app.register_blueprint(auth_bp)
    
    from .llm_change import llm_bp
    app.register_blueprint(llm_bp) 

    from app.chat import threads_bp
    app.register_blueprint(threads_bp)

    from .ui import ui_bp
    app.register_blueprint(ui_bp)

    return app
