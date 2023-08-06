import datetime
from typing import Optional
import json

import redis
from redis_om import Field, JsonModel, Migrator

from ..config import settings
from ..utils import menu2dict, submenu2dict, dish2dict
from .. import schemas
from .. import models

cache = redis.Redis(host=settings.redis_host, port=settings.redis_port, db=0)


class Menu(JsonModel):
    id: str
    title: str
    description: Optional[str]
    submenus_count: int
    dishes_count: int


class MenuCacheRepository:

    @staticmethod
    def get(id: str, item: str = "menu") -> dict:
        cached_response = cache.get(f"{item}:{id}")
        if cached_response:
            return json.loads(cached_response)
        return None

    @staticmethod
    def get_all(item: str = "menus") -> list[dict | None]:
        cached_response = cache.get(item)
        print("cached_response list: ", cached_response)
        if cached_response:
            return json.loads(cached_response)
        return []

    @staticmethod
    def add(id: str, response_orm_model: models.Menu, item: str = "menu") -> None:
        response_dict = menu2dict(response_orm_model)
        value = json.dumps(response_dict)
        key = f"{item}:{id}"
        print("cache created")
        cache.set(key, value, ex=60)

    @staticmethod
    def add_list(response_orm_model_list: list[models.Menu | None], item: str = "menus") -> None:
        values = [menu2dict(one_model)
                  for one_model in response_orm_model_list]
        key = f"{item}"
        print("cached list created")
        cache.set(key, json.dumps(values), ex=60)

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
