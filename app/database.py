from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from databases import Database

from .config import settings

# SQLACHLEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
ASYNC_SQLACHLEMY_DATABASE_URL = f'postgresql+asyncpg://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
database = Database(ASYNC_SQLACHLEMY_DATABASE_URL)

engine = create_engine(ASYNC_SQLACHLEMY_DATABASE_URL)

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# def get_db():
    # db = SessionLocal()
    # try:
        # yield db
    # finally:
        # db.close()
