from fastapi import FastAPI
from sqlalchemy_utils import create_database, database_exists

from . import models
from .database import engine, Base, init_db
from .routers import dishes, menus, submenus

# create database
# if not database_exists(engine.url):
    # create_database(engine.url)

# create tables
# Base.metadata.create_all(engine)


# # create database tables
# async def init_models():
    # async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.create_all)


app = FastAPI()

app.include_router(menus.router)
# app.include_router(submenus.router)
# app.include_router(dishes.router)

@app.on_event('startup')
async def on_startup():
    await init_db(engine)


@app.get('/api/v1/')
def root():
    return {
        'message': 'Checkout the code at https://github.com/cyrillus31/YLab_Homework-1'
    }
