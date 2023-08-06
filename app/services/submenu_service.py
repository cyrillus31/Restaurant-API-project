from typing import Union

from fastapi import Depends

from ..repositories import MenuRepository, NotificationRepository, MenuCacheRepository
from .. import schemas
from .. import models


class SubmenuService:
    def __init__(self, database_repository: MenuRepository = Depends(), ):
        self.database_repository = database_repository
        self.notificiation = NotificationRepository

    def create(self, menu_data: schemas.MenuCreate) -> models.Menu:
        new_menu = self.database_repository.add(menu_data)
        MenuCacheRepository.deinitialize_all()
        return new_menu

    def delete(self, id) -> None:
        self.database_repository.delete(id)
        MenuCacheRepository.deinitialize_all()
        return self.notificiation.delete_success()

    def get_all(self, **kwargs) -> list[models.Menu | dict]:
        cached_response = MenuCacheRepository.get_all()
        if cached_response:
            print("cache list hit")
            return cached_response
        all_menus = self.database_repository.get_all(**kwargs)
        MenuCacheRepository.add_list(all_menus)
        return all_menus

    def get(self, **kwargs) -> Union[models.Menu, dict]:
        print("looking for cache")
        cached_response = MenuCacheRepository.get(**kwargs)
        if cached_response:  # if cache exists return cached response
            print("cache hit")
            return cached_response
        menu = self.database_repository.get(
            **kwargs)  # convert ORM model into dict
        MenuCacheRepository.add(menu.id, menu)  # add dict to cache
        return menu

    def update(self, menu_data: schemas.MenuCreate, id) -> Union[models.Menu | dict]:
        update_menu = self.database_repository.update(menu_data, id)
        MenuCacheRepository.deinitialize_all()
        return update_menu
