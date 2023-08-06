from fastapi import Depends
from fastapi_cache.decorator import cache
import json

from .repositories import MenuRepository, NotificationRepository
from . import schemas
from . import models
from .cache import cache, MenuCacheRepository
from .utils import menu2dict, submenu2dict, dish2dict

# menu_add_cache({"id": "1", "title": "something",
# "dscription": "wow", "submenus_count": 10, "dishes_count": 2})


class MenuService:
    def __init__(self, database_repository: MenuRepository = Depends(), ):
        self.database_repository = database_repository
        self.notificiation = NotificationRepository

    def create(self, menu_data: schemas.MenuCreate) -> dict:
        # cached_response = MenuCacheRepository.get(menu_data)
        # if cached_response:
        # print("cahce hit")
        # return json.loads(cached_response)
        # else:
        new_menu = self.database_repository.add(menu_data)
        # MenuCacheRepository.set(menu_data, new_menu)
        return new_menu

    def delete(self, id) -> None:
        self.database_repository.delete(id)
        MenuCacheRepository.deinitialize_all()
        return self.notificiation.delete_success()

    def get_all(self, **kwargs) -> list[models.Menu]:
        cached_response = MenuCacheRepository.get_all()
        if cached_response:
            return cached_response
        all_menus = self.database_repository.get_all(**kwargs)
        return all_menus

    def get(self, **kwargs) -> models.Menu:
        cached_response = MenuCacheRepository.get(**kwargs)
        if cached_response:  # if cache exists return cached response
            return cached_response
        menu = self.database_repository.get(
            **kwargs)  # convert ORM model into dict
        MenuCacheRepository.add(menu2dict(menu))  # add dict to cache
        return menu

    def update(self, menu_data: schemas.MenuCreate, id) -> models.Menu:
        return self.database_repository.update(menu_data, id)
