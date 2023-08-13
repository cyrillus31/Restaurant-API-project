from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy_utils import create_database, database_exists

from .config import settings

SQLACHLEMY_DATABASE_URL = f'postgresql+asyncpg://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_async_engine(SQLACHLEMY_DATABASE_URL, echo=False)

async_session = sessionmaker(autocommit=False, autoflush=False, bind=engine,
                             class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

# create a database if not exists
if not database_exists(SQLACHLEMY_DATABASE_URL.replace('+asyncpg', '')):
    create_database(SQLACHLEMY_DATABASE_URL.replace('+asyncpg', ''))

# create tables


async def init_db(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
