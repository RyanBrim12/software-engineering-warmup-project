from firebase_admin import credentials, firestore, initialize_app
from google.cloud.firestore_v1.base_query import FieldFilter


class Movie:
    """Class that describes a movie."""

    def __init__(self, title, year, rating,
                 director, writer, duration, genre) -> None:
        """Initializes the instance based on given data."""
        self.title = title
        self.year = year
        self.rating = rating
        self.director = director
        self.writer = writer
        self.duration = duration
        self.genre = genre

    @staticmethod
    def from_dict(movie_dict):
        """Creates a Movie object with the data in the given dict."""
        return Movie(movie_dict["title"], movie_dict["year"],
                     movie_dict["rating"], movie_dict["director"],
                     movie_dict["writer"], movie_dict["duration"],
                     movie_dict["genre"])

    def __eq__(self, value: object) -> bool:
        """
        Returns whether the given object is equivalent to this Movie.
        """
        return (self.title == value.title
                and self.year == value.year
                and self.rating == value.rating
                and self.director == value.director
                and self.writer == value.writer
                and self.duration == value.duration
                and self.genre == value.genre)

    def __repr__(self) -> str:
        """Returns str representation of the Movie"""
        return (f"Title: {self.title}\nYear: {self.year}\n"
                f"Rating: {self.rating}\nDirector: {self.director}\n"
                f"Writer: {self.writer}\nDuration: {self.duration}\n"
                f"Genre: {self.genre}")


class FirebaseConnection:
    """
    Class for maintaing a connection and performing
    operations on the documents within a firestore database.
    """

    def __init__(self, collection_name) -> None:
        """
        Initializes and saves a connection to 
        the firestore collection of the given name.
        """
        cred = credentials.Certificate("teamOneServiceAccountKey.json")
        initialize_app(cred)
        client = firestore.client()
        self.client_connection = client.collection(collection_name)

    def complete_query(self, field, operator, value) -> list[Movie]:
        """
        Queries the firestore collection with the given parameters.
        """
        collection = self.client_connection
        query = collection.where(filter=FieldFilter(field, operator, value))
        results = query.stream()
        movies = []
        for m in results:
            movies.append(Movie.from_dict(m.to_dict()))
        return movies

    def delete_collection(self, batch_size):
        """Deletes all documents in the firestore collection."""
        if batch_size == 0:
            return

        docs = self.client_connection.list_documents(page_size=batch_size)
        deleted = 0

        for doc in docs:
            doc.delete()
            deleted = deleted + 1

        if deleted >= batch_size:
            return self.delete_collection(batch_size)

    def create_collection(self, movies: dict[str, Movie]):
        """
        Adds a document for each Movie to the firestore collection.
        """
        for id, m in movies.items():
            doc_ref = self.client_connection.document(id)
            doc_ref.set({"title": m.title, "year": m.year,
                         "rating": m.rating, "director": m.director,
                         "writer": m.writer, "duration": m.duration,
                         "genre": m.genre})


if __name__ == "__main__":
    fb = FirebaseConnection("movies")
    movies = fb.complete_query("rating", ">", 8.5)
    for m in movies:
        print(m)
