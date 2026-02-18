from flask import Flask
from dotenv import load_dotenv

from .firebase import init_firebase

def create_app():
    load_dotenv()

    app = Flask(__name__)

    init_firebase()

    @app.get("/health")
    def health():
        return "ok"

    from .auth import auth_bp
    app.register_blueprint(auth_bp) 

    return app
