import asyncio
import os
import sys

import requests
from fastapi import BackgroundTasks
from sqlalchemy import update, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from app import models

from .celery import celery_app
from .xlsx_parser import parser
from ..config import settings
from ..services import MenuService, SubmenuService, DishService


SQLACHLEMY_DATABASE_URL = f'postgresql+asyncpg://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_async_engine(SQLACHLEMY_DATABASE_URL, echo=False, pool_pre_ping=True)

async_session = sessionmaker(autocommit=False, autoflush=False, bind=engine,
                             class_=AsyncSession, expire_on_commit=False)


async def find_object(object, session, orm_model):
    query = select(orm_model).where(orm_model.id == object["id"])
    result = await session.execute(query)
    return result.scalars().first()

async def create_object(object, session, orm_model):
    new_object = orm_model(**object)
    session.add(new_object)
    await session.commit()

async def update_object(object, session, orm_model, background_tasks: BackgroundTasks):
    # update_query = update(orm_model).where(orm_model.id == object['id']).values(object)
    # await session.execute(update_query)
    # await session.commit()


# async def check_object(object, session, orm_model):
    # object_exists = await find_object(object, session, orm_model)
    # if object_exists:
        # pass
        # # await update_object(object, session, orm_model)
    # else:
        # await create_object(object, session, orm_model)

async def check_object(object, session, orm_model):
    object_exists = await find_object(object, session, orm_model)
    if not object_exists:
        await create_object(object, session, orm_model)


# async def add_to_db(objects, session, orm_model):
    # for object in objects:
        # new_object = orm_model(**object)
        # session.add(new_object)
        # await session.commit()


# async def update_menu_in_db(objects, session, orm_model):
    # for object in objects:
        # await check_object(object, session, orm_model)

async def add_to_db(objects, session, orm_model):
    for object in objects:
        await check_object(object, session, orm_model)


async def create_tables_from_excel():
    async with async_session() as session:
        await add_to_db(menus, session, models.Menu)
        await add_to_db(submenus, session, models.Submenu)
        await add_to_db(dishes, session, models.Dish)


# async def update_tables():
    # menus, submenus, dishes = parser()
    # print(menus[0])
    # async with async_session() as session:
        # await update_to_db(menus, session, models.Menu)
        # await update_to_db(submenus, session, models.Submenu)
        # await update_to_db(dishes, session, models.Dish)




@celery_app.task(name='update_db')
def update_tables_task():
    return asyncio.run(create_tables())

@celery_app.task(name='update_db')
def sync_db():
    menus, submenus, dishes = parser()

