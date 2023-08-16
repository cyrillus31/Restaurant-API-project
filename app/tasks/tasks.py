import asyncio

import aiohttp
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app import models

from ..config import settings
from .celery import celery_app
from .xlsx_parser import (
    create_temp_if_doesnt_exist,
    get_objects_to_update_create_and_to_delete,
    parser,
    update_previous_state_file,
)

PREFIX = 'api/v1/'
URL = f'http://api:8000/{PREFIX}'

SQLACHLEMY_DATABASE_URL = f'postgresql+asyncpg://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_async_engine(SQLACHLEMY_DATABASE_URL, echo=False, pool_pre_ping=True)

async_session = sessionmaker(autocommit=False, autoflush=False, bind=engine,
                             class_=AsyncSession, expire_on_commit=False)


async def find_object(object, session, orm_model):
    query = select(orm_model).where(orm_model.id == object['id'])
    result = await session.execute(query)
    return result.scalars().first()


async def create_object(object, session, orm_model):
    new_object = orm_model(**object)
    session.add(new_object)
    await session.commit()


async def check_object(object, session, orm_model):
    object_exists = await find_object(object, session, orm_model)
    if not object_exists:
        await create_object(object, session, orm_model)


async def add_to_db(objects, session, orm_model):
    for object in objects:
        await check_object(object, session, orm_model)


async def create_tables_from_excel():
    parse_results = parser()
    menus = parse_results['menus']
    submenus = parse_results['submenus']
    dishes = parse_results['dishes']
    menus = [menus[key] for key in menus]
    submenus = [submenus[key] for key in submenus]
    dishes = [dishes[key] for key in dishes]
    async with async_session() as session:
        await add_to_db(menus, session, models.Menu)
        await add_to_db(submenus, session, models.Submenu)
        await add_to_db(dishes, session, models.Dish)


async def put_request(url_key, payload):
    print('creating put connection')
    _url = URL + url_key
    print(_url)
    async with aiohttp.ClientSession() as session:
        async with session.patch(_url, json=payload) as response:
            print(response)


async def delete_request(url_key, payload):
    _url = URL + url_key
    print(_url)
    async with aiohttp.ClientSession() as session:
        async with session.delete(_url)as response:
            print(response)


async def post_request(url_key, set_id, payload):
    url_key = '/'.join(url_key.split('/')[:-1])
    _url = URL + url_key + f'/?id={set_id}'
    print(_url)
    async with aiohttp.ClientSession() as session:
        async with session.post(_url, json=payload) as response:
            print(response)


async def sync_db():
    create_temp_if_doesnt_exist()
    prev = parser(from_previous_state=True)
    curr = parser()
    print('works1')
    for type in ['menus', 'submenus', 'dishes']:
        print('works2222')
        prev_objects = prev[type]
        curr_objects = curr[type]
        d = get_objects_to_update_create_and_to_delete(prev_objects, curr_objects)
        to_update = d['update']
        to_delete = d['delete']
        to_create = d['create']
        print(d)
        print(to_create, to_delete, to_update)
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
