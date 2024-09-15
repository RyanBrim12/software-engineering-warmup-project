import json
from firebase import FirebaseConnection, Movie


def get_movies_from_file(file_name):
    with open(file_name) as f:
        file_contents = json.load(f)
    movies = []
    for movie in file_contents:
        movies.append(Movie(str(movie["ID"]), movie["Title"],
                            movie["Release Date"], movie["Rating"],
                            movie["Directed by"], movie["Written by"],
                            movie["Duration"], movie["Genres"]))
    return movies


if __name__ == "__main__":
    fb = FirebaseConnection("movies")
    movies = get_movies_from_file("movies.json")
    fb.delete_collection()
    fb.create_collection(movies)
