from typing import Union

from fastapi import Depends

from ..repositories import MenuRepository, NotificationRepository, MenuCacheRepository
from .. import schemas
from .. import models


class MenuService:
    schema = schemas.MenuCreate
    orm_model = models.Menu
    db_repository = MenuRepository

    def __init__(self, database_repository: db_repository = Depends(), ):
        self.database_repository = database_repository
        self.notificiation = NotificationRepository
        self.cache_repository = MenuCacheRepository

    def create(self, menu_data: schema, **kwargs) -> orm_model:
        new_menu = self.database_repository.add(menu_data, **kwargs)
        self.cache_repository.deinitialize_all()
        return new_menu

    def delete(self, id, **kwargs) -> None:
        self.database_repository.delete(id, **kwargs)
        self.cache_repository.deinitialize_all()
        return self.notificiation.delete_success()

    def get_all(self, **kwargs) -> list[orm_model | dict]:
        cached_response = MenuCacheRepository.get_all()
        if cached_response:
            print("cache list hit")
            return cached_response
        all_menus = self.database_repository.get_all(**kwargs)
        self.cache_repository.add_list(all_menus)
        return all_menus

    def get(self, **kwargs) -> Union[orm_model, dict]:
        print("looking for cache")
        cached_response = MenuCacheRepository.get(**kwargs)
        if cached_response:  # if cache exists return cached response
            print("cache hit")
            return cached_response
        menu = self.database_repository.get(
            **kwargs)  # convert ORM model into dict
        self.cache_repository.add(menu.id, menu)  # add dict to cache
        return menu

    def update(self, menu_data: schema, id, **kwargs) -> Union[orm_model | dict]:
        update_menu = self.database_repository.update(menu_data, id, **kwargs)
        self.cache_repository.deinitialize_all()
        return update_menu
