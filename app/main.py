from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy_utils import create_database, database_exists

from .routers import menus, submenus, dishes
from . import models
from .database import engine

# create database
if not database_exists(engine.url):
    create_database(engine.url)

# create tables
models.Base.metadata.create_all(bind=engine)


app = FastAPI()

app.include_router(menus.router)
app.include_router(submenus.router)
app.include_router(dishes.router)


@app.get("/api/vi/")
def root():
    return {"message": "This is the main page"}
