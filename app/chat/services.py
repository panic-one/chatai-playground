from app.extensions import db
from app.models.thread import Thread
from app.models.message import Message
from datetime import datetime
from zoneinfo import ZoneInfo
import threading, time
from flask import current_app

JST = ZoneInfo("Asia/Tokyo")

def create_thread(uid, title):
    title = (title or "").strip()
    if not title:
        title = datetime.now(JST).strftime("%Y-%m-%d %H:%M")
    
    th = Thread(title=title, firebase_uid=uid)
    db.session.add(th)
    db.session.commit()
    return th

def list_threads(uid):
    query = Thread.query.filter_by(firebase_uid=uid)
    query = query.order_by(Thread.created_at.desc())

    return query.all()

def get_threads(uid, thread_id):
    th = Thread.query.get(thread_id)
    if not th:
        return None, ("not found", None)
    if th.firebase_uid != uid:
        return None, ("forbidden", None)
    return th, None

def update_thread_title(uid, thread_id, new_title):
    new_title = (new_title or "").strip()
    if not new_title:
        return None, ("bad request", "title is required")
    
    th = Thread.query.get(thread_id)
    if not th:
        return None, ("not found", None)
    if th.firebase_uid != uid:
        return None, ("forbidden", None)
    
    th.title = new_title
    db.session.commit()
    return th, None

def delete_thread(uid, thread_id):
    th = Thread.query.get(thread_id)
    if not th:
        return False, ("not found", None)
    if th.firebase_uid != uid:
        return False, ("forbidden", None)
    
    Message.query.filter_by(thread_id=thread_id).delete(synchronize_session=False)

    db.session.delete(th)
    db.session.commit()
    return True, None

def ensure_thread_owner(uid, thread_id):
    th = Thread.query.get(thread_id)

    if not th:
        return None, ("not found", None)
    if th.firebase_uid != uid:
        return None, ("forbidden", None)
    return th, None

def next_message_index(thread_id: int) -> int:
    last = (
        db.session.query(db.func.max(Message.message_index))
        .filter(Message.thread_id == thread_id)
        .scalar()
    )
    return (last or 0) + 1

def create_user_message_and_ai(uid, thread_id, content):
    _, e = ensure_thread_owner(uid, thread_id)
    if e:
        return None, None, e
    
    now = datetime.now(JST)
    user_msg = Message(
        thread_id=thread_id,
        role="user",
        firebase_uid=uid,
        model=None,
        content=content,
        created_at=now,
        message_index=next_message_index(thread_id),
    )

    db.session.add(user_msg)
    db.session.flush()

    ai_msg = Message(
        thread_id=thread_id,
        role="ai",
        content="",
        firebase_uid=None,
        model="gpt-4o-mini", ##将来切り替える
        created_at=now,
        message_index=next_message_index(thread_id),
    )

    db.session.add(ai_msg)
    db.session.commit()

    app = current_app._get_current_object()
    threading.Thread(
        target=run_ai_generation,
        args=(app, ai_msg.message_id,),
        daemon=True,
    ).start()

    return user_msg, ai_msg, None

def get_message(uid, thread_id, message_id):
    _, e = ensure_thread_owner(uid, thread_id)
    if e:
        return None, e
    
    msg = Message.query.filter_by(
        message_id=message_id,
        thread_id=thread_id,
    ).first()

    if not msg:
        return None, ("not found", None)
    return msg, None

def run_ai_generation(app, message_id):
    with app.app_context():
        ai = Message.query.get(message_id)
        if not ai:
            return

    chunks = [
        "考えています",
        "回答中です",
        "回答が完成しました",
    ]

    for c in chunks:
        ai.content = (ai.content or "") + c
        db.session.commit()

        time.sleep(1)

def list_messages(uid, thread_id, limit=200, offset=0):
    _, e = ensure_thread_owner(uid, thread_id)
    if e:
        return None, e
    
    query = (
        Message.query
        .filter_by(thread_id=thread_id)
        .order_by(Message.message_index.asc(), Message.message_id.asc())
    )
    
    if offset:
        query = query.offset(int(offset))
    if limit:
        query = query.limit(int(limit))

    return query.all(), None