from flask import jsonify

def handle_error(e, not_found_message="not found"):
    if not e:
        return None
    
    kind, _ = e
    if kind == "not found":
        return jsonify({"error": not_found_message}), 404
    if kind == "forbidden":
        return jsonify({"error": "forbidden"}), 403
    return jsonify({"error": "inrernal error"}), 500