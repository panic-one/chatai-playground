from flask import Flask
from dotenv import load_dotenv
from .firebase import init_firebase
from datetime import timedelta
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

    init_firebase()

    @app.get("/health")
    def health():
        return "ok"

    from .auth import auth_bp
    app.register_blueprint(auth_bp) 

    return app
