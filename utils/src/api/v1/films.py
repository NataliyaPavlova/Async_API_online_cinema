from http import HTTPStatus

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Query
from messages.error import FilmError
from models.film import Film
from models.response_models import FilmResponseShort
from services.film import FilmService
from services.film import get_film_service

router = APIRouter()


@router.get('/search', summary='Search filmwork with words in detailed information')
async def film_search(
    q: str = Query(None, alias='query'),
    page: int = Query(1, alias='page[number]'),
    size: int = Query(50, alias='page[size]'),
    film_service: FilmService = Depends(get_film_service),
) -> list[FilmResponseShort]:
    """
    Return a list of filmworks with words in detailed information.

    Query parameters:
    - **query** - search phrase or word.

    Parameters of pagination:
    - **page[size]**: the number of elements per page.
    - **page[number]**: the number of the current page.
    """
    films = await film_service.search_objects(q, 'Film', page, size)
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=FilmError.NO_ITEM_FOR_REQUEST)
    return [FilmResponseShort.parse_obj(film) for film in films]


@router.get('/{film_id}', response_model=Film, summary='Get detailed information about one filmwork.')
async def film_details(film_id: str, film_service: FilmService = Depends(get_film_service)) -> Film:
    """
    Return detailed information about one filmwork.

    - **film_id**: uuid of filmwork.
    """
    film = await film_service.get_by_id(film_id, 'Film')
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=FilmError.ITEM_NOT_FOUND)

    return film


@router.get('/', summary='Get a list of all filmworks.')
async def films_list(
    sort_by: str = Query(None, alias='sort'),
    filter_by: str = Query(None, alias='filter[genre]'),
    page: int = Query(1, alias='page[number]'),
    size: int = Query(50, alias='page[size]'),
    film_service: FilmService = Depends(get_film_service),
) -> list[FilmResponseShort]:
    """
    Return a list of filmworks with pagination.

    Parameters of pagination:
    - **page[size]**: the number of elements per page.
    - **page[number]**: the number of the current page.

    Other parameters:
    - **sort**: Sort items by parameter. If start with '-' is descending order.
    - **filter[genre]**: Return filmworks only these genres.
    """
    # check sort params
    if sort_by and sort_by.replace('-', '') not in ['imdb_rating']:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=FilmError.WRONG_SORT_PARAMETER)
    films = await film_service.get_all_films(sort_by, filter_by, page, size)
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=FilmError.NO_ITEM_FOR_REQUEST)
    return [FilmResponseShort.parse_obj(film) for film in films]


# TODO pagination
@router.get('/{film_id}/similar', summary='Get list of similar filmworks')
async def similar_films_search(
    film_id: str,
    page: int = Query(1, alias='page[number]'),
    size: int = Query(50, alias='page[size]'),
    film_service: FilmService = Depends(get_film_service),
) -> list[FilmResponseShort]:
    """
    Return a list of similar filmworks of specified filmwork.

    Parameters:
    - **film_id**: uuid of filmwork.

    Parameters of pagination:
    - **page[size]**: the number of elements per page.
    - **page[number]**: the number of the current page.
    """
    films = await film_service.get_similar_films(film_id, page, size)
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=FilmError.NO_SIMILAR_FILM)
    return [FilmResponseShort.parse_obj(film) for film in films]
