import json

from firebase import FirebaseConnection, Movie


def get_movies_from_file(file_name):
    """
    Reads in movie information from a 
    json file and creates Movie objects.
    """
    with open(file_name) as f:
        file_contents = json.load(f)
    movies = {}
    for movie in file_contents:
        movies[str(movie["id"])] = Movie.from_dict(movie)
    return movies


if __name__ == "__main__":
    fb = FirebaseConnection("movies")
    movies = get_movies_from_file("movies.json")
    fb.delete_collection(len(movies))
    print("Deleted old collection")
    fb.create_collection(movies)
    print("Created new collection")
