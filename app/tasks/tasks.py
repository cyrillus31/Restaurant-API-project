from .xlsx_parser import parser
from app.database import async_session, engine, get_session
from app import models
import asyncio
import os
import sys

from asyncpg.exceptions import UniqueViolationError
from sqlalchemy import delete, select, update
from sqlalchemy_utils import create_database, database_exists

from .celery import celery_app

path = os.getcwd()
sys.path.append(path)


# create a database if not exists
# if not database_exists(engine.url.replace('+asyncpg', '')):
# create_database(engine.url.replace('+asyncpg', ''))


menus, submenus, dishes = parser()


@celery_app.task(name='hello')
def hello_world():
    i = random.randint(100, 300)
    print('Hello World!')

    with open(f'zzzdelete_this{i}.txt', 'w') as fire:
        fire.write('Nonething')


async def add_to_db(objects, session, orm_model):
    for object in objects:
        new_object = orm_model(**object)
        session.add(new_object)
        await session.commit()


async def update_to_db(objects, session, orm_model):
    for object in objects:
        update_query = update(orm_model).where(orm_model.id == object['id']).values(object)
        await session.execute(update_query)
        await session.commit()


async def create_tables():
    async with async_session() as session:
        await add_to_db(menus, session, models.Menu)
        await add_to_db(submenus, session, models.Submenu)
        await add_to_db(dishes, session, models.Dish)


async def update_tables():
    async with async_session() as session:
        await update_to_db(menus, session, models.Menu)
        await update_to_db(submenus, session, models.Submenu)
        await update_to_db(dishes, session, models.Dish)


@celery_app.task(name='create_db')
def create_tables_task():
    return asyncio.run(create_tables())


@celery_app.task(name='update_db')
def update_tables_task():
    return asyncio.run(update_tables())
