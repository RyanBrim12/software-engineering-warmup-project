import json
from firebase import get_firebase_connection


def create_collection():
    with open("movies.json") as f:
        file_contents = json.load(f)
    for movie in file_contents:
        doc_ref = db.collection("movies").document(f"{movie["ID"]}")
        doc_ref.set({"title": movie["Title"], "release": movie["Release Date"],
                     "rating": movie["Rating"], "director": movie["Directed by"],
                     "writer": movie["Written by"], "duration": movie["Duration"]})

# TODO: implement function
def delete_collection():
    pass

if __name__ == "__main__":
    db = get_firebase_connection()
    delete_collection()
    create_collection()