from .base import BaseOrjsonModelWithUUID


class GenreInFilm(BaseOrjsonModelWithUUID):
    name: str


class PersonInFilm(BaseOrjsonModelWithUUID):
    full_name: str


class Film(BaseOrjsonModelWithUUID):
    title: str
    imdb_rating: float | None
    description: str | None
    genre: list[GenreInFilm]
    directors: list[PersonInFilm]
    actors: list[PersonInFilm]
    writers: list[PersonInFilm]
