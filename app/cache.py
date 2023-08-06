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


class Menu(JsonModel):
    id: str
    title: str
    description: Optional[str]
    submenus_count: int
    dishes_count: int


class MenuCacheRepository:
    @staticmethod
    def add(menu: dict):
        new_menu = Menu(**menu)
        new_menu.save()
        new_menu.expire(30)

    @staticmethod
    def get(id: str):
        menu = Menu.find(Menu.id == id).first()
        return menu

    @staticmethod
    def get_all():
        menus = Menu.find(Menu.id != 1).all()
        return menus

    # @staticmethod
    # def get(key: schemas.MenuCreate):
        # cached_response = cache.get(json.dumps(key.dict()))
        # return cached_response

    # @staticmethod
    # def set_one(request: schemas.MenuCreate, response_orm_model: models.Menu):
        # response_dict = menu2dict(response_orm_model)
        # key = json.dumps(request.dict())
        # value = json.dumps(response_dict)
        # print("cache created")
        # cache.set(key, value, ex=30)

    # @staticmethod
    # def set_list(request: dict, response_orm_list: list[models.Menu | None]):
        # response_dict = [menu2dict(model) for model in response_orm_list]
        # key = json.dumps(request.dict())
        # value = json.dumps(response_dict)
        # print("cache created")
        # cache.set(key, value, ex=30)

    @staticmethod
    def deinitialize_all():
        cache.flushall()


class Submenu(JsonModel):
    # id: Field(primary_key=True)
    title: str
    description: Optional[str]
    dishes_count: int


class Dish(JsonModel):
    # id: Field(primary_key=True)
    title: str
    description: Optional[str]
    price: str


def menu_add_cache(menu: dict):
    new_menu = Menu(**menu)
    new_menu.save()
    new_menu.expire(30)
