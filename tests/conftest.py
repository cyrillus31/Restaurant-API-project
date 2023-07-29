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

from app import models


# from alembic import command


# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:password123@localhost:5432/fastapi_test'
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"


engine = create_engine(SQLALCHEMY_DATABASE_URL)

# creating test database
if not database_exists(engine.url):
    create_database(engine.url)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# test route setup
@pytest.fixture(autouse=True, scope="session")
def PREFIX():
    return "/api/v1"


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


# create test models using SQL
@pytest.fixture(scope="function")
def test_menus(session):
    posts_data = [
        {"title": "test post 1", "description": "description of test post 1"},
        {"title": "test post 2", "description": "description of test post 2"},
        {"title": "test post 3", "description": "description of test post 3"},
    ]
    new_menus = [models.Menu(**post) for post in posts_data]
    session.add_all(new_menus)
    session.commit()

    db_new_menus_list = session.query(models.Menu).all()
    return db_new_menus_list
