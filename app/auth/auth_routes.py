from flask import jsonify, render_template, request, session
from . import auth_bp
from .auth_services import verify_firebase_token

@auth_bp.get("/me")
def me():
    uid, err = verify_firebase_token()
    if err:
        return jsonify({"error": str(err)}), 401
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

@auth_bp.get("/home")
def home():
    uid = session.get("uid")
    if not uid:
        return jsonify({"error": "Unauthorized"}), 401
    return render_template("home.html", uid=uid)

@auth_bp.post("/session")
def create_session():
    data = request.get_json(silent=True) or {}
    id_token = data.get("idToken")
    if not id_token:
        return jsonify({"error": "missing idToken"}), 400
    
    uid, err = verify_firebase_token(id_token)
    if err:
        return jsonify({"error": str(err)}), 401
    
    session["uid"] = uid
    return jsonify({"ok": True, "uid": uid}), 200

@auth_bp.post("/logout")
def logout():
    session.clear()
    return ("", 204)