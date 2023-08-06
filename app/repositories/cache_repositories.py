import json

import redis  # type: ignore

from .. import models
from ..config import settings
from ..utils import dish2dict, menu2dict, submenu2dict

cache = redis.Redis(host=settings.redis_host, port=settings.redis_port, db=0)


class MenuCacheRepository:
    # object = 'menu'
    # objects = 'menus'
    # orm_model = models.Menu
    # to_dict_func = menu2dict

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

    def get(self, id: str, **kwargs) -> dict | None:
        cached_response = cache.get(f'{self.object}:{id}')
        if cached_response:
            return json.loads(cached_response)
        return None

    def get_all(self, **kwargs) -> list[dict | None]:

        # generate key from kwargs
        key = f'{self.objects}'
        for k in kwargs:
            key += str(kwargs[k])

        cached_response = cache.get(key)
        print('cached_response list: ', cached_response)
        if cached_response:
            return json.loads(cached_response)
        return []

    def add(self, id: str, response_orm_model: models.Menu | models.Submenu | models.Dish | None) -> None:
        response_dict = self.to_dict_func(response_orm_model)  # type: ignore
        value = json.dumps(response_dict)
        key = f'{self.object}:{id}'
        print('cache created')
        cache.set(key, value, ex=60)

    def add_list(self, response_orm_model_list: list[models.Menu | models.Submenu | models.Dish | None], **kwargs) -> None:
        values = [self.to_dict_func(one_model)  # type: ignore
                  for one_model in response_orm_model_list]

        # generate key from kwargs
        key = f'{self.objects}:'
        for k in kwargs:
            key = key + str(kwargs[k])

        print('cached list created')
        cache.set(key, json.dumps(values), ex=60)

    @classmethod
    def deinitialize_all(cls):
        cache.flushall()


# Other Cahce Repositories via Inheritance


class SubmenuCacheRepository(MenuCacheRepository):
    pass
    # object = 'submenu'
    # objects = 'submenus'
    # orm_model = models.Submenu
    # to_dict_func = submenu2dict


class DishCacheRepository(MenuCacheRepository):
    pass
    # object = 'dish'
    # objects = 'dishes'
    # orm_model = models.Dish
    # to_dict_func = dish2dict
