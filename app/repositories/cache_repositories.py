import json

import redis  # type: ignore

from .. import models
from ..config import settings
from ..utils import dish2dict, menu2dict, submenu2dict

cache = redis.Redis(host=settings.redis_host, port=settings.redis_port, db=0)

CACHE_EXPIRE_TIME = 1000


class MenuCacheRepository:

    def __init__(self, object, objects):
        self.object = object
        self.objects = objects

        # choose a function to convert
        if object == 'menu':
            self.to_dict_func = menu2dict
        if object == 'submenu':
            self.to_dict_func = submenu2dict
        if object == 'dish':
            self.to_dict_func = dish2dict

    def get(self, url_key: str) -> dict | None:
        key = url_key
        cached_response = cache.get(key)
        if cached_response:
            return json.loads(cached_response)
        return None

    def get_all(self, url_key: str) -> list[dict | None]:

        # generate key from kwargs
        key = url_key

        cached_response = cache.get(key)
        print('cached_response list: ', cached_response)
        if cached_response:
            return json.loads(cached_response)
        return []

    def add(self, url_key: str, response_orm_model: models.Menu | models.Submenu | models.Dish | None) -> None:
        response_dict = self.to_dict_func(response_orm_model)  # type: ignore
        value = json.dumps(response_dict)
        key = url_key
        print('cache created')
        cache.set(key, value, ex=CACHE_EXPIRE_TIME)

    def add_list(self, url_key: str, response_orm_model_list: list[models.Menu | models.Submenu | models.Dish | None]) -> None:
        values = [self.to_dict_func(one_model)  # type: ignore
                  for one_model in response_orm_model_list]

        # generate key from kwargs
        key = url_key

        print('cached list created')
        cache.set(key, json.dumps(values), ex=CACHE_EXPIRE_TIME)

    def invalidate_update_cache(self, id):
        """This methods deletes cached list the updated http resource belongs to"""
        r1 = cache.delete(*cache.keys(f'*{self.objects}/'))
        r2 = cache.delete(*cache.keys(f'*{self.objects}/{id}/'))
        print('the following objects were suppose to be  deleted: \n',
              f'*{self.objects}/\n',
              f'*{self.objects}/{id}/')
        print(r1, r2)

    def invalidate_all_related_cache(self, url_key):
        split_url = url_key.split('/')
        url_to_delete = ''
        for resource in split_url:
            if resource == '':
                continue
            url_to_delete += f'{resource}/'
            cache.delete(url_to_delete)
            print(f'cached object {url_to_delete} was deleted')

    @classmethod
    def deinitialize_all(cls):
        cache.flushall()


# Other Cahce Repositories via Inheritance


class SubmenuCacheRepository(MenuCacheRepository):
    pass


class DishCacheRepository(MenuCacheRepository):
    pass
