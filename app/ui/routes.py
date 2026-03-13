from flask import Blueprint, jsonify, render_template
from . import ui_bp
from app.auth.auth_services import verify_firebase_token

@ui_bp.route("/chatai-playground", methods=["GET"])
def home():
    return render_template("home.html")