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


class MenuCacheRepository:
    object = "menu"
    objects = "menus"
    orm_model = models.Menu
    to_dict_func = menu2dict

    @classmethod
    def get(cls, id: str, item: str = object) -> dict:
        cached_response = cache.get(f"{item}:{id}")
        if cached_response:
            return json.loads(cached_response)
        return None

    @classmethod
    def get_all(cls, item: str = objects, **kwargs) -> list[dict | None]:

        # generate key from kwargs
        key = f"{item}"
        for k in kwargs:
            key += str(kwargs[k])

        cached_response = cache.get(key)
        print("cached_response list: ", cached_response)
        if cached_response:
            return json.loads(cached_response)
        return []

    @classmethod
    def add(cls, id: str, response_orm_model: orm_model, item: str = object) -> None:
        response_dict = cls.to_dict_func(response_orm_model)
        value = json.dumps(response_dict)
        key = f"{item}:{id}"
        print("cache created")
        cache.set(key, value, ex=60)

    @classmethod
    def add_list(cls, response_orm_model_list: list[orm_model | None], item: str = objects, **kwargs) -> None:
        values = [cls.to_dict_func(one_model)
                  for one_model in response_orm_model_list]

        # generate key from kwargs
        key = f"{item}"
        for k in kwargs:
            key += str(kwargs[k])

        print("cached list created")
        cache.set(key, json.dumps(values), ex=60)

    @classmethod
    def deinitialize_all(cls):
        cache.flushall()


class SubmenuCacheRepository(MenuCacheRepository):
    object = "submenu"
    objects = "submenus"
    orm_model = models.Submenu
    to_dict_func = submenu2dict
