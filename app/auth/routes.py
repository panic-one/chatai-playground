from flask import jsonify, render_template
from . import auth_bp
from .services import verify_firebase_token

@auth_bp.get("/me")
def me():
    uid, err = verify_firebase_token()
    if err:
        return jsonify({"error": err}), 401
    return jsonify({"uid": uid}), 200

@auth_bp.get("/login")
def login():
    firebase_config = {
        "apiKey": "AIzaSyBgpRpnqsvLDnWrgffQeEaU-2I5BFHPJTk",
        "authDomain": "chatai-playground.firebaseapp.com",
        "projectId": "chatai-playground",
        "appId": "1:747369968863:web:75b240f4ca396c20bfe56a",
        "messagingSenderId": "747369968863",
    }
    return render_template("login.html", firebase_config=firebase_config)