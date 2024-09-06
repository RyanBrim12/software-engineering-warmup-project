import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


def get_firebase_connection():
    cred = credentials.Certificate('serviceAccountKey.json')
    app = firebase_admin.initialize_app(cred)
    db = firestore.client()
    return db
