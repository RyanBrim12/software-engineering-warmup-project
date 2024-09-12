import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

class Movie:
    def __init__(self, id, title, release_date, rating,
                 directors, writers, duration, genres) -> None:
        self.id = id
        self.title = title
        self.release_date = release_date
        self.rating = rating
        self.directors = directors
        self.writers = writers
        self.duration = duration
        self.genres = genres



class Firebase_Connection:
    def __init__(self) -> None:
        cred = credentials.Certificate('serviceAccountKey.json')
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()


    def complete_query(field, operator, value):
        pass


    def delete_collection(self):
        pass


    def create_collection(self, movies):
        for m in movies:
            doc_ref = self.db.collection("movies").document(f"{m.id}")
            doc_ref.set({"title": m.title, "release": m.release_date,
                         "rating": m.rating, "directors": m.directors,
                         "writers": m.writers, "duration": m.duration,
                         "genres": m.genres})