import os
import sys
import asyncio

from sqlalchemy import select, update, delete
from sqlalchemy_utils import database_exists, create_database
from asyncpg.exceptions import UniqueViolationError

path = os.getcwd()
sys.path.append(path)

from xlsx_parser import parser
from app.database import async_session, get_session, engine
from app import models

# create a database if not exists
# if not database_exists(engine.url.replace('+asyncpg', '')):
    # create_database(engine.url.replace('+asyncpg', ''))

menus, submenus, dishes = parser()

async def add_to_db(objects, session, orm_model):
    for object in objects:
        new_object = orm_model(**object)
        session.add(new_object)
        await session.commit()

async def update_to_db(objects, session, orm_model):
    for object in objects:
        update_query = update(orm_model).where(orm_model.id == object["id"]).values(object)
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

asyncio.run(create_tables())

asyncio.run(update_tables())
