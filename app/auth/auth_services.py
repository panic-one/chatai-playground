from flask import request
from firebase_admin import auth
from flask import session, jsonify

def verify_firebase_token(id_token: str | None = None):
    if not id_token:
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return None, "Missing Bearer token"
        id_token = auth_header[len("Bearer "):].strip()

    # uidを取得できたらuidを返して、失敗したらerrを返す
    try:
        decoded = auth.verify_id_token(id_token)
        uid = decoded.get("uid")
        if not uid:
            return None, "uid not found in token"
        return uid, None
    except Exception as err:
        return None, err
    
def require_login():
    uid = session.get("uid")
    if not uid:
        return None, (jsonify({"error": "Unauthorized"}), 401)
    return uid, None
