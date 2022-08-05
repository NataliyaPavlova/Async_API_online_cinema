from http import HTTPStatus

from fastapi import APIRouter
from fastapi import Depends, Query
from fastapi import HTTPException
from messages.error import PersonError
from models.person import Person
from models.response_models import FilmResponseShort
from services.person import PersonService
from services.person import get_person_service

router = APIRouter()


@router.get('/search')
async def search_persons(
    q: str = Query(None, alias='query'),
    page: int = Query(1, alias='page[number]'),
    size: int = Query(50, alias='page[size]'),
    person_service: PersonService = Depends(get_person_service),
) -> list[Person]:
    persons = await person_service.search_objects(q, 'Person', page, size)
    if not persons:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=PersonError.NO_ITEM)
    return persons


@router.get('/{person_id}', response_model=Person, summary='Get detailed information about one person.')
async def person_details(person_id: str, person_service: PersonService = Depends(get_person_service)) -> Person:
    """
    Return detailed information about one person.

    - **person_id**: uuid of person.
    """
    person = await person_service.get_by_id(person_id, 'Person')
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=PersonError.ITEM_NOT_FOUND)

    return person


@router.get('/{person_id}/film', summary='Get list of filmworks with specified person')
async def get_person_films(
    person_id: str, person_service: PersonService = Depends(get_person_service)
) -> list[FilmResponseShort]:
    """
    Return list of filmworks with specified person.

    - **person_id**: uuid of person.
    """
    films = await person_service.get_films_by_id(person_id)
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=PersonError.FILMS_NOT_FOUND)
    return [FilmResponseShort.parse_obj(film) for film in films]
