from typing import Union

from fastapi import Depends

from ..repositories import MenuRepository, SubmenuRepository, NotificationRepository, MenuCacheRepository, SubmenuCacheRepository
from .. import schemas
from .. import models
from .menu_service import MenuService


class SubmenuService(MenuService):
    schema = schemas.SubmenuCreate
    orm_model = models.Submenu
    db_repository = SubmenuRepository

    def __init__(self, database_repository: db_repository = Depends(), ):
        self.database_repository = database_repository
        self.notificiation = NotificationRepository("submenu")
        self.cache_repository = SubmenuCacheRepository

    # def create(self, menu_data: schemas.MenuCreate, **kwargs) -> models.Menu:
        # new_menu = self.database_repository.add(menu_data, **kwargs)
        # MenuCacheRepository.deinitialize_all()
        # return new_menu

    # def delete(self, id, **kwargs) -> None:
        # self.database_repository.delete(id, **kwargs)
        # MenuCacheRepository.deinitialize_all()
        # return self.notificiation.delete_success()

    # def get_all(self, **kwargs) -> list[models.Menu | dict]:
        # cached_response = MenuCacheRepository.get_all()
        # if cached_response:
        # print("cache list hit")
        # return cached_response
        # all_menus = self.database_repository.get_all(**kwargs)
        # MenuCacheRepository.add_list(all_menus)
        # return all_menus

    # def get(self, **kwargs) -> Union[models.Menu, dict]:
        # print("looking for cache")
        # cached_response = MenuCacheRepository.get(**kwargs)
        # if cached_response:  # if cache exists return cached response
        # print("cache hit")
        # return cached_response
        # menu = self.database_repository.get(
        # **kwargs)  # convert ORM model into dict
        # MenuCacheRepository.add(menu.id, menu)  # add dict to cache
        # return menu

    # def update(self, menu_data: schemas.MenuCreate, id, **kwargs) -> Union[models.Menu | dict]:
        # update_menu = self.database_repository.update(menu_data, id, **kwargs)
        # MenuCacheRepository.deinitialize_all()
        # return update_menu
