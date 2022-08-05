from enum import Enum


class FilmError(str, Enum):
    NO_ITEM_FOR_REQUEST = 'No films found based on your request'
    ITEM_NOT_FOUND = 'The film is not found'
    NO_SIMILAR_FILM = 'No similar films found'
    WRONG_SORT_PARAMETER = 'Wrong sort parameter'


class GenreError(str, Enum):
    NO_ITEM = 'No genres found'
    ITEM_NOT_FOUND = 'The genre is not found'
    NO_POPULAR_FILMS = 'No popular films for the genre'


class PersonError(str, Enum):
    NO_ITEM = 'No persons found'
    ITEM_NOT_FOUND = 'The person is not found'
    FILMS_NOT_FOUND = 'No films found for this person'
