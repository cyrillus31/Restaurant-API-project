import asyncio

import aiohttp

from .celery import celery_app
from .xlsx_parser import (
    create_temp_if_doesnt_exist,
    get_objects_to_update_create_and_to_delete,
    parser,
    update_previous_state_file,
)

PREFIX = 'api/v1/'
URL = f'http://api:8000/{PREFIX}'


async def put_request(url_key, payload):
    _url = URL + url_key
    async with aiohttp.ClientSession() as session:
        async with session.patch(_url, json=payload) as response:
            print(response)


async def delete_request(url_key, payload):
    _url = URL + url_key
    async with aiohttp.ClientSession() as session:
        async with session.delete(_url)as response:
            print(response)


async def post_request(url_key, set_id, payload):
    url_key = '/'.join(url_key.split('/')[:-1])
    _url = URL + url_key + f'/?id={set_id}'
    async with aiohttp.ClientSession() as session:
        async with session.post(_url, json=payload) as response:
            print(response)


async def sync_db():
    create_temp_if_doesnt_exist()
    prev = parser(from_previous_state=True)
    curr = parser()
    for type in ['menus', 'submenus', 'dishes']:
        prev_objects = prev[type]
        curr_objects = curr[type]
        d = get_objects_to_update_create_and_to_delete(prev_objects, curr_objects)
        to_update = d['update']
        to_delete = d['delete']
        to_create = d['create']
        for url_key in to_update:
            await put_request(url_key, to_update[url_key])
            print(f'{url_key} was updated!')
        for url_key in to_delete:
            await delete_request(url_key, to_delete[url_key])
            print(f'{url_key} was deleted!')
        for url_key in to_create:
            set_id = to_create[url_key]['id']
            await post_request(url_key, set_id, to_create[url_key])
            print(f'{url_key} was created!')

    update_previous_state_file()


@celery_app.task(name='update_db')
def update_tables_task():
    return asyncio.run(sync_db())
