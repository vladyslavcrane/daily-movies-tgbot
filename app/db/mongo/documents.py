from typing import List
from beanie import Document

class Moovie(Document):
    title: str
    release_year: int
    director: str
    plot: str
    genres: List[str]
    actors: List[str]
    imdb_link: str
    imdb_rating: float
    posted: bool = False

    class Settings:
        name = "moovies"