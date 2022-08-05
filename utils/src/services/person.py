from functools import lru_cache

from aioredis import Redis
from db.elastic import get_elastic
from db.redis import get_redis
from elasticsearch import AsyncElasticsearch
from elasticsearch import NotFoundError
from fastapi import Depends
from models.film import Film
from models.person import Person

from .film import BaseService


class PersonService(BaseService):
    async def get_films_by_id(self, person_id: str) -> list[Film]:
        cache_key = f'Person__get_films_by_person__{person_id}'
        films = await self._list_from_cache(cache_key, 'Film')
        if not films:
            films = await self._get_person_films_from_elastic(person_id)
            await self._put_list_to_cache(films, cache_key)
        if not films:
            return []
        return films

    async def _get_person_films_from_elastic(self, person_id: str) -> list[Film]:
        try:
            # get the persons' film_ids
            doc = await self.elastic.get('persons', person_id)
            person = Person(**doc['_source'])

            # get films by ids from 'movies' index
            films = await self.elastic.mget(index='movies', body={'ids': person.film_ids})
            docs = []
            for film in films['docs']:
                docs.append(Film(**film['_source']))
        except NotFoundError:
            return []
        return docs


@lru_cache()
def get_person_service(
    redis: Redis = Depends(get_redis), elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonService:
    return PersonService(redis, elastic)
