import os
import firebase_admin
from firebase_admin import credentials

def init_firebase():
    if not firebase_admin._apps:
        path = os.getenv("FIREBASE_SERVICE_ACCOUNT_PATH")
        if not path:
            raise RuntimeError("FIREBASE_SERVICE_ACCOUNT_PATH が未設定です")
        cred = credentials.Certificate(path)
        firebase_admin.initialize_app(cred)
