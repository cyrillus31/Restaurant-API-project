import asyncio
from collections.abc import Generator
from typing import AsyncGenerator

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists

from app import models
from app.config import settings
from app.database import Base, get_session
from app.main import app
from app.repositories import MenuCacheRepository

ASYNC_SQLACHLEMY_DATABASE_URL = f'postgresql+asyncpg://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

if not database_exists(ASYNC_SQLACHLEMY_DATABASE_URL.replace('+asyncpg', '')):
    create_database(ASYNC_SQLACHLEMY_DATABASE_URL.replace('+asyncpg', ''))

async_engine = create_async_engine(ASYNC_SQLACHLEMY_DATABASE_URL, echo=False,)

testing_async_session = sessionmaker(autocommit=False, autoflush=False,
                                     bind=async_engine, class_=AsyncSession, expire_on_commit=False)


@pytest.fixture(autouse=True, scope='session')
def PREFIX() -> str:
    return '/api/v1'


@pytest.fixture(autouse=True, scope='function')  # test empty cache
async def empty_cache() -> None:
    await MenuCacheRepository.deinitialize_all()


@pytest.fixture(scope='session')
def anyio_backend() -> str:
    return 'asyncio'


@pytest.fixture(scope='function')
async def session() -> AsyncGenerator:
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with testing_async_session() as session:
        yield session

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope='session')
def event_loop() -> Generator:
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture()
async def client() -> AsyncGenerator[AsyncClient, None]:
    async def override_get_async_session():
        async with testing_async_session() as session:
            yield session
    app.dependency_overrides[get_session] = override_get_async_session
    async with AsyncClient(app=app, base_url='http://test/') as ac:
        yield ac


"""
Creating test models in database

#######################################


TEST DATABASE STRUCTURE using fixtures


Restaurant


Restaurant
├── Menu 1
│   ├── Submenu 1
│   │   ├── Dish 1
│   │   └── Dish 2
│   └── Submenu 2
│       └── Dish 3
├── Menu 2
│   └── Submenu 3
└── Menu 3

#######################################

"""


@pytest.fixture(scope='function')
async def test_menus(session: AsyncSession) -> list[models.Menu]:
    menus_data = [
        {'title': 'test menu 1', 'description': 'description of test menu 1'},
        {'title': 'test menu 2', 'description': 'description of test menu 2'},
        {'title': 'test menu 3', 'description': 'description of test menu 3'},
    ]

    new_menus = [models.Menu(**menu) for menu in menus_data]
    session.add_all(new_menus)
    await session.commit()
    result = await session.execute(select(models.Menu))
    db_new_menus_list = result.scalars().all()
    return db_new_menus_list


@pytest.fixture(scope='function')
async def test_submenus(session: AsyncSession, test_menus: list[models.Menu]) -> list[models.Submenu]:
    menu1_id = test_menus[0].id
    menu2_id = test_menus[1].id
    # menu3_id = test_menus[2].id
    submenus_data = [
        {
            'title': 'test submenu 1-1',
            'description': 'description of test submenu 1 in main menu 1',
            'menu_id': menu1_id,
        },
        {
            'title': 'test submenu 1-2',
            'description': 'description of test submenu 2 in main menu 1',
            'menu_id': menu1_id,
        },
        {
            'title': 'test submenu 2-3',
            'description': 'description of test submenu 3 in main menu 2',
            'menu_id': menu2_id,
        },

    ]

    new_submenus = [models.Submenu(**submenu) for submenu in submenus_data]
    session.add_all(new_submenus)
    await session.commit()
    result = await session.execute(select(models.Submenu))
    db_new_submenus_list = result.scalars().all()
    return db_new_submenus_list


@pytest.fixture(scope='function')
async def test_dishes(session: AsyncSession, test_menus: list[models.Menu], test_submenus: list[models.Submenu]) -> list[models.Dish]:
    menu_id = test_menus[0].id
    result = (
        await session.execute(select(models.Submenu).filter(
            models.Submenu.menu_id == menu_id))
    )
    related_submenus = result.scalars().all()

    submenu1_id = related_submenus[0].id
    submenu2_id = related_submenus[1].id
    dishes_data = [
        {
            'title': 'test dish 1-1-1',
            'description': 'description of test dish 1 in  submenu 1',
            'price': '120.35',
            'submenu_id': submenu1_id,
        },

        {
            'title': 'test dish 1-1-2',
            'description': 'description of test dish 2 in  submenu 1',
            'price': '1.40',
            'submenu_id': submenu1_id,
        },

        {
            'title': 'test submenu 1-2-3',
            'description': 'description of test dish 3 in  submenu 2',
            'price': '20.45',
            'submenu_id': submenu2_id,
        },

    ]

    new_dishes = [models.Dish(**dish) for dish in dishes_data]
    session.add_all(new_dishes)
    await session.commit()
    result = await session.execute(select(models.Dish))
    db_new_dishes_list = result.scalars().all()
    return db_new_dishes_list
