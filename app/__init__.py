from flask import Flask
from dotenv import load_dotenv
from .firebase import init_firebase
import os

def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret")

    init_firebase()

    @app.get("/health")
    def health():
        return "ok"

    from .auth import auth_bp
    app.register_blueprint(auth_bp) 

    return app
