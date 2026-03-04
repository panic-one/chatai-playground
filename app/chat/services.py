from app.extensions import db
from app.models.thread import Thread
from app.models.message import Message
from datetime import datetime
from zoneinfo import Zoneinfo

JST = Zoneinfo("Asia/Tokyo")

def create_thread(uid, title):
    title = (title or "").strip()
    if not title:
        title = datetime.now(JST).strftime("%Y-%m-%d %H:%M")
    
    th = Thread(title=title, owner_uid=uid)
    db.session.add(th)
    db.session.commit()
    return th

def list_threads(uid):
    que = Thread.query.filter_by(owner_uid=uid)

    try:
        que = que.order_by(Thread.created_at.desc())
    except Exception:
        que = que.order_by(Thread.id.desc())

    return que.all()

def get_threads(uid, thread_id):
    th = Thread.query.get(thread_id)
    if not th:
        return None, ("not found", None)
    if th.owner_uid != uid:
        return None, ("forbidden", None)
    return th, None

def update_thread_title(uid, thread_id, new_title):
    new_title = (new_title or "").strip()
    if not new_title:
        return None, ("bad request", "title is required")
    
    th = Thread.query.get(thread_id)
    if not th:
        return None, ("not found", None)
    if th.owner_uid != uid:
        return None, ("forbidden", None)
    
    th.title = new_title
    db.session.commit()
    return th, None

def delete_thread(uid, thread_id):
    th = Thread.query.get(thread_id)
    if not th:
        return False, ("not found", None)
    if th.owner_uid != uid:
        return False, ("forbidden", None)
    
    Message.query.filter_by(thread_id=thread_id).delete(synchronize_session=False)

    db.session.delete(th)
    db.session.commit()
    return True, None