import datetime
from typing import Optional
import json

import redis
from redis_om import Field, JsonModel, Migrator

from .config import settings
from .utils import menu2dict, submenu2dict, dish2dict
from . import schemas
from . import models

cache = redis.Redis(host=settings.redis_host, port=settings.redis_port, db=0)


class MenuCacheRepository:
    @staticmethod
    def get(key: schemas.MenuCreate):
        cached_response = cache.get(json.dumps(key.dict()))
        return cached_response

    @staticmethod
    def set_one(request: schemas.MenuCreate, response_orm_model: models.Menu):
        response_dict = menu2dict(response_orm_model)
        key = json.dumps(request.dict())
        value = json.dumps(response_dict)
        print("cache created")
        cache.set(key, value, ex=30)

    @staticmethod
    def set_list(request: dict, response_orm_list: list[models.Menu | None]):
        response_dict = [menu2dict(model) for model in response_orm_list]
        key = json.dumps(request.dict())
        value = json.dumps(response_dict)
        print("cache created")
        cache.set(key, value, ex=30)

    @staticmethod
    def deinitialize_all():
        cache.flushall()


class Menu(JsonModel):
    id: str
    title: str
    description: Optional[str]
    submenus_count: int
    dishes_count: int


class Submenu(JsonModel):
    id: str
    title: str
    description: Optional[str]
    dishes_count: int


class Dish(JsonModel):
    id: str
    title: str
    description: Optional[str]
    price: str


def menu_add_cache(menu: dict):
    new_menu = Menu(**menu)
    new_menu.save()
    new_menu.expire(30)
