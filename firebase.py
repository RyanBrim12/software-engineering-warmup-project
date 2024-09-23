import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud.firestore_v1.base_query import FieldFilter

class Movie:
    def __init__(self, id, title, release, rating,
                 director, writer, duration, genre) -> None:
        self.id = id
        self.title = title
        self.release = release
        self.rating = rating
        self.director = director
        self.writer = writer
        self.duration = duration
        self.genre = genre

    
    @staticmethod
    def from_dict(dict):
        return Movie(str(dict["id"]), dict["title"], dict["release"],
                     dict["rating"], dict["director"], dict["writer"],
                     dict["duration"], dict["genre"])


    def __repr__(self) -> str:
        return (f"Title: {self.title}\nRelease Date: {self.release}\n"
                f"Rating: {self.rating}\nDirector: {self.director}\n"
                f"Writer: {self.writer}\nDuration: {self.duration}\n"
                f"Genre: {self.genre}")


class FirebaseConnection:
    def __init__(self, collection_name) -> None:
        cred = credentials.Certificate("teamOneServiceAccountKey.json")
        firebase_admin.initialize_app(cred)
        self.client_connection = firestore.client().collection(collection_name)


    def complete_query(self, field, operator, value) -> list[Movie]:
        collection = self.client_connection
        query = collection.where(filter=FieldFilter(field, operator, value))
        results = query.stream()
        movies = []
        for m in results:
            movies.append(Movie.from_dict(m.to_dict()))
        return movies


    def delete_collection(self, batch_size):
        if batch_size == 0:
            return

        docs = self.client_connection.list_documents(page_size=batch_size)
        deleted = 0

        for doc in docs:
            doc.delete()
            deleted = deleted + 1

        if deleted >= batch_size:
            return self.delete_collection(batch_size)


    def create_collection(self, movies):
        for m in movies:
            doc_ref = self.client_connection.document(m.id)
            doc_ref.set({"title": m.title, "release": m.release,
                         "rating": m.rating, "director": m.director,
                         "writer": m.writer, "duration": m.duration,
                         "genre": m.genre})
            

if __name__ == "__main__":
    fb = FirebaseConnection("movies")
    movies = fb.complete_query("rating", ">", 8.5)
    for m in movies:
        print(m)