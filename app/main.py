from fastapi import FastAPI
from sqlalchemy_utils import create_database, database_exists

from . import models
from .database import engine, database
from .routers import menus, submenus, dishes 

# create database
if not database_exists(engine.url):
    create_database(engine.url)

# create tables
models.Base.metadata.create_all(bind=engine)


app = FastAPI()

app.include_router(menus.router)
app.include_router(submenus.router)
app.include_router(dishes.router)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def disconnect():
    await database.disconnect()


@app.get('/api/v1/')
async def root():
    return {
        'message': 'Checkout the code at https://github.com/cyrillus31/YLab_Homework-1'
    }

