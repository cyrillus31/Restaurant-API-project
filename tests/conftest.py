from typing import AsyncGenerator

import asyncio
import pytest

from httpx import AsyncClient

from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker 
from sqlalchemy_utils import create_database, database_exists
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from app import models
from app.config import settings
from app.database import Base, get_session 
from app.main import app
from app.repositories import MenuCacheRepository


SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

ASYNC_SQLACHLEMY_DATABASE_URL = f'postgresql+asyncpg://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

async_engine = create_async_engine(ASYNC_SQLACHLEMY_DATABASE_URL, echo=True,) 

testing_async_session = sessionmaker(autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession, expire_on_commit=False)


# creating test database
# if not database_exists(engine.url):
    # create_database(engine.url)
@pytest.fixture()
def client():
    client = TestClient(app)
    return client

@pytest.fixture()
def session():
    print('my session fixture ran')
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(autouse=True, scope='session')
def PREFIX():
    return '/api/v1'

@pytest.fixture(autouse=True, scope='function')  # test empty cache
def empty_cache():
    MenuCacheRepository.deinitialize_all()

@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"

@pytest.fixture(scope='function')
async def async_session():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield testing_async_session
    # yield async_engine

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

# let test session to know it is running inside event loop
@pytest.fixture(scope='session')
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()

# async def client(session):
@pytest.fixture()
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    async def override_get_async_session():
        async with testing_async_session() as session:
            yield session
    app.dependency_overrides[get_session] = override_get_async_session
    async with AsyncClient(app=app, base_url="http://test/") as ac:
        yield ac


"""
Creating test models in database

#######################################


TEST DATABASE STRUCTURE using fixtures


Restaurant



├── Menu 1
│   ├── Submenu 1
│   │   ├── Dish 1
│   │   └── Dish 2
│   └── Submenu 2
│       └── Dish 3
└── Menu 2
    └── Submenu 3

#######################################

"""



@pytest.fixture(scope='function')
async def test_menus(session):
    menus_data = [
        {'title': 'test menu 1', 'description': 'description of test menu 1'},
        {'title': 'test menu 2', 'description': 'description of test menu 2'},
        {'title': 'test menu 3', 'description': 'description of test menu 3'},
    ]


    new_menus = [models.Menu(**menu) for menu in menus_data]
    session.add_all(new_menus)
    session.commit()
    db_new_menus_list = session.query(models.Menu).all()
    return db_new_menus_list



# @pytest.fixture(scope='function')
# def test_submenus(async_session, test_menus):
    # menu1_id = test_menus[0].id
    # menu2_id = test_menus[1].id
    # # menu3_id = test_menus[2].id
    # submenus_data = [
        # {
            # 'title': 'test submenu 1-1',
            # 'description': 'description of test submenu 1 in main menu 1',
            # 'menu_id': menu1_id,
        # },
        # {
            # 'title': 'test submenu 1-2',
            # 'description': 'description of test submenu 2 in main menu 1',
            # 'menu_id': menu1_id,
        # },
        # {
            # 'title': 'test submenu 2-3',
            # 'description': 'description of test submenu 3 in main menu 2',
            # 'menu_id': menu2_id,
        # },

    # ]

    # new_submenus = [models.Submenu(**submenu) for submenu in submenus_data]
    # async_session.add_all(new_submenus)
    # async_session.commit()
    # db_new_submenus_list = async_session.query(models.Submenu).all()
    # return db_new_submenus_list



# @pytest.fixture(scope='function')
# def test_dishes(async_session, test_menus, test_submenus):
    # menu_id = test_menus[0].id
    # related_submenus = (
        # async_session.query(models.Submenu).filter(
            # models.Submenu.menu_id == menu_id).all()
    # )


    # submenu1_id = related_submenus[0].id
    # submenu2_id = related_submenus[1].id
    # dishes_data = [
        # {
            # 'title': 'test dish 1-1-1',
            # 'description': 'description of test dish 1 in  submenu 1',
            # 'price': '120.35',
            # 'submenu_id': submenu1_id,
        # },

        # {
            # 'title': 'test dish 1-1-2',
            # 'description': 'description of test dish 2 in  submenu 1',
            # 'price': '1.40',
            # 'submenu_id': submenu1_id,
        # },

        # {
            # 'title': 'test submenu 1-2-3',
            # 'description': 'description of test dish 3 in  submenu 2',
            # 'price': '20.45',
            # 'submenu_id': submenu2_id,
        # },

    # ]


    # new_dishes = [models.Dish(**dish) for dish in dishes_data]
    # async_session.add_all(new_dishes)
    # async_session.commit()
    # db_new_dishes_list = async_session.query(models.Dish).all()

    # return db_new_dishes_list

