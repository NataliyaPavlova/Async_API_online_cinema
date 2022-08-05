import json
from functools import lru_cache
from typing import Any
from typing import Optional
import sys
from aioredis import Redis
from db.elastic import get_elastic
from db.redis import get_redis
from elasticsearch import AsyncElasticsearch
from elasticsearch import NotFoundError
from fastapi import Depends
from models.film import Film
from models.genre import Genre
from models.person import Person
from pydantic.json import pydantic_encoder
from pydantic import parse_raw_as

FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 минут


class BaseService:

    # model name <-> Elastic index name
    mapping = {
        'Film': 'movies',
        'Genre': 'genres',
        'Person': 'persons',
    }

    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def get_by_id(self, object_id: str, model_name: str) -> Optional:
        object_ = await self._object_from_cache(object_id, model_name)
        if not object_:
            object_ = await self._get_object_from_elastic(object_id, model_name)
        if not object_:
            return None
        await self._put_object_to_cache(object_, object_.uuid)
        return object_

    async def _get_object_from_elastic(self, object_id: str, model_name: str) -> Optional:
        try:
            index = BaseService.mapping[model_name]
            doc = await self.elastic.get(index, object_id)
        except NotFoundError:
            return None
        return getattr(sys.modules[__name__], model_name)(**doc['_source'])

    async def search_objects(self, query: str, model_name: str, page: int, size: int) -> list:
        """Get objects by search query"""
        cache_key = f'{model_name}__search__{query}__{page}__{size}'
        objects = await self._list_from_cache(cache_key, model_name)
        if not objects:
            objects = await self._search_objects_in_elastic(query, model_name, page, size)
            await self._put_list_to_cache(objects, cache_key)
        return objects

    async def _search_objects_in_elastic(self, query: str, model_name: str, page: int, page_size: int) -> list:
        docs = []
        query_body = {'query': {'query_string': {'query': query}}}
        page = page if page else 1
        page_size = page_size if page_size else 50
        index = BaseService.mapping[model_name]
        try:
            hits = await self.elastic.search(index=index, body=query_body, size=page_size, from_=(page - 1) * page_size)
            for hit in hits['hits']['hits']:
                docs.append(getattr(sys.modules[__name__], model_name)(**hit['_source']))
        except NotFoundError:
            return []
        return docs

    async def _object_from_cache(self, cache_key: str, model_name: str) -> Optional[Any]:
        data = await self.redis.get(cache_key)
        if not data:
            return None
        object_ = getattr(sys.modules[__name__], model_name).parse_raw(data)
        return object_

    async def _list_from_cache(self, cache_key: str, model_name: str) -> list[Any]:
        data = await self.redis.get(cache_key)
        if not data:
            return []
        objects_ = parse_raw_as(list[getattr(sys.modules[__name__], model_name)], data)
        return objects_

    async def _put_object_to_cache(self, object_: Any, cache_key: str):
        await self.redis.set(cache_key, object_.json(), expire=FILM_CACHE_EXPIRE_IN_SECONDS)

    async def _put_list_to_cache(self, object_: list, cache_key: str):
        json_list = json.dumps(object_, default=pydantic_encoder)
        await self.redis.set(cache_key, json_list, expire=FILM_CACHE_EXPIRE_IN_SECONDS)


class FilmService(BaseService):
    async def get_all_films(self, sort_by: Optional[str], filter_by: Optional[str], page: int, size: int) -> list[Film]:
        """Get all films from index"""
        cache_key = f'Film__get_all__{sort_by}__{filter_by}__{page}__{size}'
        films = await self._list_from_cache(cache_key, 'Film')
        if not films:
            films = await self._get_films_sort_filter(sort_by, filter_by, page, size)
            await self._put_list_to_cache(films, cache_key)
        return films

    async def _get_films_sort_filter(
        self, sort_by: Optional[str], filter_by: Optional[str], page: int, size: int
    ) -> list[Film]:
        """Get all films with given sort and filter"""
        try:
            body = {}
            if sort_by:
                order = 'desc' if sort_by[0] == '-' else 'asc'
                body['sort'] = [{sort_by: {'order': order}}]
            if filter_by:
                body['query'] = {
                    'nested': {'path': 'genre', 'query': {'bool': {'must': [{'match': {'genre.name': filter_by}}]}}}
                }
            hits = await self.elastic.search(index='movies', body=body, from_=(page - 1) * size, size=size)
            docs = []
            for hit in hits['hits']['hits']:
                docs.append(Film(**hit['_source']))
        except NotFoundError:
            return []
        return docs

    async def get_similar_films(self, film_id: str, page: int, size: int) -> list[Film]:
        """Get similar films with a given film"""
        cache_key = 'Film__get_similar'
        films = await self._list_from_cache(cache_key, 'Film')
        if not films:
            films = await self._get_films_of_same_genre(film_id, page, size)
            await self._put_list_to_cache(films, cache_key)
        return films

    async def _get_films_of_same_genre(self, film_id, page: int, size: int) -> list[Film]:
        """Get films having at least one common genre with a given film"""
        try:
            film = await self._get_object_from_elastic(film_id, 'Film')
            shoulds = [{'match': {'genre.name': g.name}} for g in film.genre]
            search_body = {
                'query': {
                    'nested': {'path': 'genre', 'query': {'bool': {'should': shoulds, 'minimum_should_match': 1}}}
                }
            }
            hits = await self.elastic.search(index='movies', body=search_body, size=page, from_=size * (page - 1))
            docs = []
            for hit in hits['hits']['hits']:
                docs.append(Film(**hit['_source']))
        except NotFoundError:
            return []
        return docs


@lru_cache()
def get_film_service(
    redis: Redis = Depends(get_redis), elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(redis, elastic)
