import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import json

# Use a service account.
cred = credentials.Certificate('serviceAccountKey.json')

app = firebase_admin.initialize_app(cred)

db = firestore.client()

with open("movies.json") as f:
    file_contents = json.load(f)
for movie in file_contents:
    doc_ref = db.collection("movies").document(f"{movie["ID"]}")
    doc_ref.set({"title": movie["Title"], "release": movie["Release Date"], "rating": movie["Rating"], "director": movie["Directed by"], "writer": movie["Written by"], "duration": movie["Duration"]})