from functools import lru_cache

from aioredis import Redis
from db.elastic import get_elastic
from db.redis import get_redis
from elasticsearch import AsyncElasticsearch
from elasticsearch import NotFoundError
from fastapi import Depends
from models.genre import Genre
from models.film import Film
from .film import BaseService


class GenreService(BaseService):
    async def get_genres(self, page: int, size: int) -> list[Genre]:
        """Get all genres from index"""
        cache_key = f'get_all_genres_{page}_{size}'
        genres = await self._list_from_cache(cache_key, 'Genre')
        if not genres:
            genres = await self._get_genres(page, size)
            await self._put_list_to_cache(genres, cache_key)
        return genres

    async def _get_genres(self, page: int, size: int) -> list[Genre]:
        try:
            body = {}
            hits = await self.elastic.search(index='genres', body=body, size=size, from_=(page - 1) * size)
            docs = []
            for hit in hits['hits']['hits']:
                docs.append(Genre(**hit['_source']))
        except NotFoundError:
            return []
        return docs

    async def get_films_by_id(self, genre_id: str, page: int, size: int) -> list[Film]:
        cache_key = f'Genre__get_films_by_genre_id__{genre_id}__{page}__{size}'
        films = await self._list_from_cache(cache_key, 'Film')
        if not films:
            films = await self._get_films_from_elastic(genre_id, page, size)
            await self._put_list_to_cache(films, cache_key)
        if not films:
            return []
        return films

    async def _get_films_from_elastic(self, genre_id: str, page: int, size: int) -> list[Film]:
        body = {
            'sort': [{'imdb_rating': {'order': 'desc'}}],
            'query': {'nested': {'path': 'genre', 'query': {'bool': {'must': [{'match': {'genre.uuid': genre_id}}]}}}},
        }
        try:
            hits = await self.elastic.search(index='movies', body=body, size=size, from_=(page - 1) * size)
            docs = []
            for hit in hits['hits']['hits']:
                docs.append(Film(**hit['_source']))
        except NotFoundError:
            return []
        return docs


@lru_cache()
def get_genre_service(
    redis: Redis = Depends(get_redis), elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(redis, elastic)
