import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database

from app.main import app
from app.config import settings
from app.database import get_db
from app.database import Base
from app.cache import MenuCacheRepository

from app import models


# from alembic import command


# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:password123@localhost:5432/fastapi_test'
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"


engine = create_engine(SQLALCHEMY_DATABASE_URL)

# creating test database
if not database_exists(engine.url):
    create_database(engine.url)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


# test route setup
@pytest.fixture(autouse=True, scope="session")
def PREFIX():
    return "/api/v1"


@pytest.fixture(autouse=True, scope="function")  # test empty cache
def empty_cache():
    MenuCacheRepository.deinitialize_all()


@pytest.fixture()
def session():
    print("my session fixture ran")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


"""
Creating test models in database

#######################################
TEST DATABASE STRUCTURE using fixtures 

data_test/
├─ test menu 1/
│  ├─ submenu 1-1/
│  │  ├─ dish 1-1-1
│  │  ├─ dish 1-1-2
│  ├─ submenu 1-2/
│  │  ├─ dish 1-2-3
├─ test menu 2/
│  ├─ submenu 2-3/
├─ test menu3/

#######################################
"""


@pytest.fixture(scope="function")
def test_menus(session):
    menus_data = [
        {"title": "test menu 1", "description": "description of test menu 1"},
        {"title": "test menu 2", "description": "description of test menu 2"},
        {"title": "test menu 3", "description": "description of test menu 3"},
    ]
    new_menus = [models.Menu(**menu) for menu in menus_data]
    session.add_all(new_menus)
    session.commit()

    db_new_menus_list = session.query(models.Menu).all()
    return db_new_menus_list


@pytest.fixture(scope="function")
def test_submenus(session, test_menus):
    menu1_id = test_menus[0].id
    menu2_id = test_menus[1].id
    # menu3_id = test_menus[2].id

    submenus_data = [
        {
            "title": "test submenu 1-1",
            "description": "description of test submenu 1 in main menu 1",
            "menu_id": menu1_id,
        },
        {
            "title": "test submenu 1-2",
            "description": "description of test submenu 2 in main menu 1",
            "menu_id": menu1_id,
        },
        {
            "title": "test submenu 2-3",
            "description": "description of test submenu 3 in main menu 2",
            "menu_id": menu2_id,
        },
    ]
    new_submenus = [models.Submenu(**submenu) for submenu in submenus_data]
    session.add_all(new_submenus)
    session.commit()

    db_new_submenus_list = session.query(models.Submenu).all()
    return db_new_submenus_list


@pytest.fixture(scope="function")
def test_dishes(session, test_menus, test_submenus):
    menu_id = test_menus[0].id
    # menu2_id = test_menus[1].id
    # menu3_id = test_menus[2].id
    related_submenus = (
        session.query(models.Submenu).filter(
            models.Submenu.menu_id == menu_id).all()
    )
    submenu1_id = related_submenus[0].id
    submenu2_id = related_submenus[1].id

    dishes_data = [
        {
            "title": "test dish 1-1-1",
            "description": "description of test dish 1 in  submenu 1",
            "price": "120.35",
            "submenu_id": submenu1_id,
        },
        {
            "title": "test dish 1-1-2",
            "description": "description of test dish 2 in  submenu 1",
            "price": "1.40",
            "submenu_id": submenu1_id,
        },
        {
            "title": "test submenu 1-2-3",
            "description": "description of test dish 3 in  submenu 2",
            "price": "20.45",
            "submenu_id": submenu2_id,
        },
    ]
    new_dishes = [models.Dish(**dish) for dish in dishes_data]
    session.add_all(new_dishes)
    session.commit()

    db_new_dishes_list = session.query(models.Dish).all()
    return db_new_dishes_list
