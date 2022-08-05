from http import HTTPStatus

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Query
from messages.error import GenreError
from models.genre import Genre
from models.response_models import FilmResponseShort
from services.genre import GenreService
from services.genre import get_genre_service

router = APIRouter()


@router.get('/', summary='Get a list of all genres.')
async def get_genres(
    page: int = Query(1, alias='page[number]'),
    size: int = Query(50, alias='page[size]'),
    genre_service: GenreService = Depends(get_genre_service),
) -> list[Genre]:
    """
    Return a list of genres with pagination.

    Parameters of pagination:
    - **page[size]**: the number of elements per page.
    - **page[number]**: the number of the current page.
    """
    genres = await genre_service.get_genres(page, size)
    if not genres:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=GenreError.NO_ITEM)
    return genres


@router.get('/{genre_id}', response_model=Genre, summary='Get detailed information about one genre.')
async def genre_details(genre_id: str, genre_service: GenreService = Depends(get_genre_service)) -> Genre:
    """
    Return detailed information about one genre.

    - **genre_id**: uuid of genre.
    """
    genre = await genre_service.get_by_id(genre_id, 'Genre')
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=GenreError.ITEM_NOT_FOUND)

    return genre


@router.get('/{genre_id}/popular', summary='Get most popular filmworks of specified genre.')
async def genre_details_popular(
    genre_id: str,
    page: int = Query(1, alias='page[number]'),
    size: int = Query(50, alias='page[size]'),
    genre_service: GenreService = Depends(get_genre_service),
) -> list[FilmResponseShort]:
    """
    Return a list of most popular filmworks of specified genre.

    Parameters of pagination:
    - **page[size]**: the number of elements per page.
    - **page[number]**: the number of the current page.
    """
    films = await genre_service.get_films_by_id(genre_id, page, size)
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=GenreError.NO_POPULAR_FILMS)

    return [FilmResponseShort.parse_obj(film) for film in films]
