import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud.firestore_v1.base_query import FieldFilter

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

    
    def __repr__(self) -> str:
        return (f"Title: {self.title}\nRelease Date: {self.release_date}\n"
                f"Rating: {self.rating}\nDirectors: {self.directors}\n"
                f"Writers: {self.writers}\nDuration: {self.duration}\n"
                f"Genres: {self.genres}")


class FirebaseConnection:
    def __init__(self, collection_name) -> None:
        cred = credentials.Certificate('serviceAccountKey.json')
        firebase_admin.initialize_app(cred)
        self.client_connection = firestore.client()
        self.collection_name = collection_name


    def complete_query(self, field, operator, value) -> list[Movie]:
        collection = self.client_connection.collection(self.collection_name)
        query = collection.where(filter=FieldFilter(field, operator, value))
        results = query.stream()
        movies = []
        for m in results:
            m_dict = m.to_dict()
            movies.append(Movie(None, m_dict["title"],
                            m_dict["release"], m_dict["rating"],
                            m_dict["directors"], m_dict["writers"],
                            m_dict["duration"], m_dict["genres"]))
        return movies


    def delete_collection(self, batch_size):
        if batch_size == 0:
            return

        docs = self.client_connection.collection(self.collection_name).list_documents(page_size=batch_size)
        deleted = 0

        for doc in docs:
            print(f"Deleting doc {doc.id} => {doc.get().to_dict()}")
            doc.delete()
            deleted = deleted + 1

        if deleted >= batch_size:
            return self.delete_collection(batch_size)


    def create_collection(self, movies):
        for m in movies:
            doc_ref = self.client_connection.collection(self.collection_name).document(m.id)
            doc_ref.set({"title": m.title, "release": m.release_date,
                         "rating": m.rating, "directors": m.directors,
                         "writers": m.writers, "duration": m.duration,
                         "genres": m.genres})
            

if __name__ == "__main__":
    fb = FirebaseConnection("movies")
    movies = fb.complete_query("rating", ">", 8.5)
    for m in movies:
        print(m)