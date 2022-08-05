from .base import BaseOrjsonModelWithUUID


class Genre(BaseOrjsonModelWithUUID):
    name: str
    description: str | None
    popularity: int | None
