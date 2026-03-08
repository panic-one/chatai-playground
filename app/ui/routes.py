from flask import Blueprint, jsonify, render_template
from . import ui_bp
from app.auth.auth_services import verify_firebase_token

@ui_bp.route("/chatai-playground", methods=["GET"])
def home():

    firebase_config = {
        "apiKey": "AIzaSyBgpRpnqsvLDnWrgffQeEaU-2I5BFHPJTk",
        "authDomain": "chatai-playground.firebaseapp.com",
        "projectId": "chatai-playground",
        "appId": "1:747369968863:web:75b240f4ca396c20bfe56a",
        "messagingSenderId": "747369968863",
    }

    return render_template(
        "home.html",
        firebase_config=firebase_config
    )