from flask import request, jsonify
from . import threads_bp
from app.extensions import db
from app.auth.auth_routes import require_login
from . import services


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
def get_thread(thread_id: str):
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
def update_title(thread_id: str):
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
def delete_thread(thread_id: str):
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