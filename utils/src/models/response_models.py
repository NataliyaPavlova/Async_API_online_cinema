from .base import BaseOrjsonModelWithUUID


class FilmResponseShort(BaseOrjsonModelWithUUID):
    title: str
    imdb_rating: float | None
