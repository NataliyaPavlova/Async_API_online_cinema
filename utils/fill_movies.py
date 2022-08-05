import json
from string import Template

import asyncio
from elasticsearch import AsyncElasticsearch
from faker import Faker
import uuid
from random import randint, random
from pprint import pprint
import requests

#es = AsyncElasticsearch(hosts=[f'{config.ELASTIC_HOST}:{config.ELASTIC_PORT}'])
#es = AsyncElasticsearch(hosts={'127.0.0.1:9200'})

fake = Faker()


def get_fake_film() -> dict:
    genres = [{"uuid": str(uuid.uuid4()), "name": fake.language_name()} for _ in range(randint(1, 10))]
    directors = [{"uuid": str(uuid.uuid4()), "full_name": fake.name()}]
    actors = [{"uuid": str(uuid.uuid4()), "full_name": fake.name()} for _ in range(randint(1, 10))]
    writers = [{"uuid": str(uuid.uuid4()), "full_name": fake.name()} for _ in range(randint(1, 3))]

    actors_name = [item['full_name'] for item in actors]
    writers_name = [item['full_name'] for item in writers]

    return {
        "uuid": str(uuid.uuid4()),
        "imdb_rating": random() * 10,
        "genre": genres,
        "title": fake.sentence(nb_words=randint(1, 10)),
        "description": fake.sentence(nb_words=randint(10, 100)),
        "directors": directors,
        "actors": actors,
        "writers": writers,
        "actors_names": actors_name,
        "writers_names": writers_name,
    }


template_es = Template(
    '{"index": {"_index": "movies", "_id": "$id"} }\n$item\n'
)


N = 200000
part_size = 1000
headers = {'Content-Type': 'application/x-ndjson'}

for _ in range(N//part_size):
    print(_, end="")
    json_items = []
    for _ in range(part_size):
        item = get_fake_film()
        item_json = json.dumps(item)
        es_json = template_es.substitute(
            id=item['uuid'], item=item_json)
        json_items.append(es_json)
    es_data = "".join(json_items)

    response = requests.post(
        'http://es:9200/_bulk?filter_path=items.*.error',
        headers=headers,
        data=es_data
    )
    print(response.json())
print('All done.')


# async def main():
#     item = get_fake_film()
#     body = template_es.substitute(item=item, id=item['id'])
#
    # resp = await es.create(
    #     index="movies",
    #     id=item['id'],
    #     body=item,
    # )
    # print(resp)


# loop = asyncio.new_event_loop()
# loop.run_until_complete(main())
