## What is it:

Async API for online cinema with no registration

## What is in it:

1. FastAPI async API to get data about movies, genres, persons
2. Advanced search with Elasticsearch
3. Fake movies data generation

## How to start

docker-compose up -d --build
(You may need data in Elasticsearch to see how it works)

## Documentation

http://0.0.0.0/api/openapi

## To generate fake data in ES:

1. docker-compose exec app /bin/bash
2. /utils/create_indexes.sh
3. /utils/fill_movies.py

## Stack:

Async FastAPI, Elasticsearch, Docker Compose, Redis
