import json

import redis  # type: ignore
from redis import asyncio as aioredis

from .. import models
from ..config import settings
from ..utils import dish2dict, menu2dict, submenu2dict

cache = aioredis.Redis(host=settings.redis_host, port=settings.redis_port, db=0)

CACHE_EXPIRE_TIME = 60  # seconds


class TreeCacheRepository:
    """FOR ADDING ALL MENUS, SUBMENUS AND DISHES"""
    @staticmethod
    async def get_tree(url_key: str) -> dict | None:
        key = url_key
        cached_response = await cache.get(key)
        if cached_response:
            return json.loads(cached_response)
        return None

    @staticmethod
    async def add_tree(url_key: str, dict_to_store: dict) -> None:
        key = url_key
        print('cached list created')
        await cache.set(key, json.dumps(dict_to_store), ex=CACHE_EXPIRE_TIME)

    @staticmethod
    async def drop_tree(url_key: str = 'getall/') -> None:
        try:
            await cache.delete(url_key)

        except redis.exceptions.ResponseError as e:
            print(e)


class MenuCacheRepository:

    def __init__(self, object: str, objects: str):
        self.object = object
        self.objects = objects

        # choose a function to convert
        if object == 'menu':
            self.to_dict_func = menu2dict
        if object == 'submenu':
            self.to_dict_func = submenu2dict
        if object == 'dish':
            self.to_dict_func = dish2dict

    async def get(self, url_key: str) -> dict | None:
        key = url_key
        cached_response = await cache.get(key)
        if cached_response:
            return json.loads(cached_response)
        return None

    async def get_all(self, url_key: str) -> list[dict | None] | None:

        # generate key from kwargs
        key = url_key

        cached_response = await cache.get(key)
        print('cached_response list: ', cached_response)
        if cached_response:
            return json.loads(cached_response)
        return None

    async def add(self, url_key: str, response_orm_model: models.Menu | models.Submenu | models.Dish | None) -> None:
        response_dict = self.to_dict_func(response_orm_model)  # type: ignore
        value = json.dumps(response_dict)
        key = url_key
        print('cache created')
        await cache.set(key, value, ex=CACHE_EXPIRE_TIME)

    async def add_list(self, url_key: str, response_orm_model_list: list[models.Menu | models.Submenu | models.Dish | None]) -> None:
        values = [self.to_dict_func(one_model)  # type: ignore
                  for one_model in response_orm_model_list]

        # generate key from kwargs
        key = url_key

        print('cached list created')
        await cache.set(key, json.dumps(values), ex=CACHE_EXPIRE_TIME)

    async def invalidate_update_cache(self, id: str):
        """This methods deletes cached list the updated http resource belongs to"""

        await TreeCacheRepository.drop_tree()
        # in case someone tries to update empty cache entires
        try:
            await cache.delete(*await cache.keys(f'*{self.objects}/'))
            await cache.delete(*await cache.keys(f'*{self.objects}/{id}/'))
            print('the following objects were suppose to be  deleted: \n',
                  f'*{self.objects}/\n',
                  f'*{self.objects}/{id}/')
        except redis.exceptions.ResponseError as e:
            print(e)

    async def invalidate_all_related_cache(self, url_key: str):

        await TreeCacheRepository.drop_tree()

        try:
            split_url = url_key.split('/')
            url_to_delete = ''
            for resource in split_url:
                if resource == '':
                    continue
                url_to_delete += f'{resource}/'
                await cache.delete(url_to_delete)
                print(f'cached object {url_to_delete} was deleted')
            keys_to_delete = await cache.keys(url_to_delete + '*')
            await cache.delete(*keys_to_delete)

        except redis.exceptions.ResponseError as e:
            print(e)

    @classmethod
    async def deinitialize_all(cls):
        await cache.flushall()


# Other Cahce Repositories via Inheritance


class SubmenuCacheRepository(MenuCacheRepository):
    pass


class DishCacheRepository(MenuCacheRepository):
    pass
