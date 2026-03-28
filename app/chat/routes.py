from flask import request, jsonify, g
from . import threads_bp
from app.auth.auth_services import verify_firebase_token
from . import services
from app.services import handle_error
from app.llm.services import stream_ai_response_with_meta
import logging

logger = logging.getLogger(__name__)

@threads_bp.before_request
def authenticate():
    uid, err = verify_firebase_token()
    if err:
        return jsonify({"error": str(err)}), 401
    g.uid = uid

@threads_bp.post("")
def create_thread():
    payload = request.get_json(silent=True) or {}
    title = payload.get("title")

    th = services.create_thread(g.uid, title)
    return jsonify(th.to_dict()), 201

@threads_bp.get("")
def list_threads():
    threads = services.list_threads(g.uid)
    return jsonify([t.to_dict() for t in threads]), 200

@threads_bp.get("/<int:thread_id>")
def get_thread(thread_id: int):
    th, e = services.get_thread(g.uid, thread_id)
    err_res = handle_error(e, "thread not found")
    if err_res:
        return err_res
    return jsonify(th.to_dict()), 200

@threads_bp.patch("/<int:thread_id>")
def update_title(thread_id: int):
    payload = request.get_json(silent=True) or {}
    new_title = (payload.get("title") or "").strip()
    if not new_title:
        return jsonify({"error": "title is required"}), 400
    
    th, e = services.update_thread_title(g.uid, thread_id, new_title)
    err_res = handle_error(e, "thread not found")
    if err_res:
        return err_res
        
    return  jsonify(th.to_dict()), 200

@threads_bp.delete("/<int:thread_id>")
def delete_thread(thread_id: int):
    ok, e = services.delete_thread(g.uid, thread_id)
    err_res = handle_error(e, "thread not found")
    if err_res:
        return err_res
        
    return jsonify({"deleted": True, "id": thread_id}), 200

@threads_bp.post("/<int:thread_id>/messages")
def post_message(thread_id: int):
    payload = request.get_json(silent=True) or {}
    content = (payload.get("content") or "").strip()
    provider = (payload.get("provider") or "auto").strip()

    if not content:
        return jsonify({"error": "content is required"}), 400
    
    try:
        _, selection, analysis = stream_ai_response_with_meta(
            user_message=content,
            provider=provider,
        )
    except ValueError as err:
        return jsonify({"error": str(err)}), 400
    except Exception as err:
        logger.exception("LLM routing failed during post_message")
        return jsonify({"error": "llm routing failed"}), 500
    
    user_msg, ai_msg, e = services.create_user_message_and_ai(g.uid, thread_id, content, selection.provider, selection.model)
    err_res = handle_error(e, "message not found")
    if err_res:
        return err_res
        
    return jsonify({
        "user": user_msg.to_dict(),
        "ai": ai_msg.to_dict(),
        "llm": {
            "provider": selection.provider,
            "model": selection.model,
            "score": selection.score,
            "routing_mode": selection.routing_mode,
            "category": analysis.category,
            "difficulty": analysis.difficulty,
            "reason": analysis.reason,
        }
    }), 202


@threads_bp.get("/<int:thread_id>/messages/<int:message_id>")
def get_message(thread_id: int, message_id: int):
    msg, e = services.get_message(g.uid, thread_id, message_id)
    err_res = handle_error(e, "thread not found")
    if err_res:
        return err_res
    return jsonify(msg.to_dict()), 200

@threads_bp.get("/<int:thread_id>/messages")
def list_messages(thread_id: int):
    limit = request.args.get("limit", type=int)
    offset = request.args.get("offset", type=int)
    messages, e = services.list_messages(g.uid, thread_id, limit=limit, offset=offset)
    err_res = handle_error(e, "thread not found")
    if err_res:
        return err_res
        
    return jsonify([m.to_dict() for m in messages]), 200