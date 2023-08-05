from fastapi import FastAPI
from sqlalchemy_utils import create_database, database_exists

from .routers import menus, submenus, dishes
from . import models
from .database import engine
from .config import settings

# from fastapi_cache import FastAPICache
# from fastapi_cache.backends.redis import RedisBackend
# from fastapi_cache.decorator import cache
# from redis import asyncio as aioredis

# create database
if not database_exists(engine.url):
    create_database(engine.url)

# create tables
models.Base.metadata.create_all(bind=engine)


app = FastAPI()

app.include_router(menus.router)
app.include_router(submenus.router)
app.include_router(dishes.router)


@app.get("/api/v1/")
def root():
    return {
        "message": "Checkout the code at https://github.com/cyrillus31/YLab_Homework-1"
    }
