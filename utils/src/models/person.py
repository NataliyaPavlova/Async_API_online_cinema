from enum import Enum
from .base import BaseOrjsonModelWithUUID


class Person(BaseOrjsonModelWithUUID):
    class PersonType(str, Enum):
        actor = 'actor'
        director = 'director'
        writer = 'writer'

    full_name: str
    film_ids: list[str] | None
    role: PersonType | None

    class Config:
        use_enum_values = True
