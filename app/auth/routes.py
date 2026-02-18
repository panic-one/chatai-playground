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
    return render_template("login.html")
