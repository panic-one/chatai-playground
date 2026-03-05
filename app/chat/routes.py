from flask import request, jsonify, render_template
from . import threads_bp
from app.extensions import db
from app.auth.auth_services import require_login
from . import services

@threads_bp.route("/home", methods=["GET"])
def home():
    uid = require_login()
    if not uid:
        return jsonify({"error": "Unauthorized"}), 401
    return render_template("home.html", uid=uid)

@threads_bp.post("")
def create_thread():
    uid, err = require_login()
    if err:
        return err
    

    payload = request.get_json(silent=True) or {}
    title = payload.get("title")

    th = services.create_thread(uid, title)
    return jsonify(th.to_dict()), 201

@threads_bp.get("")
def list_threads():
    uid, err = require_login()
    if err:
        return err
    
    threads = services.list_threads(uid)
    return jsonify([t.to_dict() for t in threads]), 200

@threads_bp.get("/<thread_id>")
def get_thread(thread_id: int):
    uid, err = require_login()
    if err:
        return err
    
    th, e = services.get_thread(uid, thread_id)
    if e:
        kind, _ = e
        if kind == "not found":
            return jsonify({"error": "thread not found"}), 404
        if kind == "forbidden":
            return jsonify({"error": "forbidden"}), 403
        
    return jsonify(th.to_dict()), 200

@threads_bp.patch("/<thread_id>")
def update_title(thread_id: int):
    uid, err = require_login()
    if err:
        return err
    
    payload = request.get_json(silent=True) or {}
    new_title = (payload.get("title") or "").strip()
    if not new_title:
        return jsonify({"error": "title is required"}), 400
    
    th, e = services.update_thread_title(uid, thread_id, new_title)
    if e:
        kind, _ = e
        if kind == "not found":
            return jsonify({"error": "thread not found"}), 404
        if kind == "forbidden":
            return jsonify({"error": "forbidden"}), 403
        
    return  jsonify(th.to_dict()), 200

@threads_bp.delete("/<thread_id>")
def delete_thread(thread_id: int):
    uid, err = require_login()
    if err:
        return err
    
    ok, e = services.delete_thread(uid, thread_id)
    if e:
        kind, _ = e
        if kind == "not found":
            return jsonify({"error": "thread not found"}), 404
        if kind == "forbidden":
            return jsonify({"error": "forbidden"}), 403
        
    return jsonify({"deleted": True, "id": thread_id}), 200

@threads_bp.post("/<thread_id>/messages")
def post_message(thread_id):
    uid, err = require_login()
    if err:
        return err
    
    payload = request.get_json(silent=True) or {}
    content = (payload.get("content") or "").strip()

    if not content:
        return jsonify({"error": "content is required"}), 400
    
    user_msg, ai_msg, e = services.create_user_message_and_ai(uid, thread_id, content)
    if e:
        kind, _ = e
        if kind == "not found":
            return jsonify({"error": "thread not found"}), 404
        if kind == "forbidden":
            return jsonify({"error": "forbidden"}), 403
        
    return jsonify({
        "user": user_msg.to_dict(),
        "ai": ai_msg.to_dict()
    }), 201


@threads_bp.get("/<thread_id>/messages/<message_id>")
def get_message(thread_id, message_id):
    uid, err = require_login()
    if err:
        return err
    
    msg, e = services.get_message(uid, thread_id, message_id)
    if e:
        kind, _ = e
        if kind == "not found":
            return jsonify({"error": "message not found"}), 404
        if kind == "forbidden":
            return jsonify({"error": "forbidden"}), 403
    return jsonify(msg.to_dict()), 200

@threads_bp.get("/<thread_id>/messages")
def list_messages(thread_id):
    uid, err = require_login()
    if err:
        return err
    
    messages, e = services.list_messages(uid, thread_id)
    if e:
        kind, _ = e
        if kind == "not found":
            return jsonify({"error": "thread not found"}), 403
        if kind == "forbidden":
            return jsonify({"error": "forbidden"}), 403
        
    return jsonify([m.to_dict() for m in messages]), 200