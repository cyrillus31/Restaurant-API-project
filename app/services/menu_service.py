from fastapi import Depends

from .. import models, schemas
from ..repositories import MenuCacheRepository, MenuRepository, NotificationRepository


class MenuService:
    schema = schemas.MenuCreate
    orm_model = models.Menu
    db_repository = MenuRepository

    def __init__(self, database_repository: MenuRepository = Depends(), ) -> None:
        self.database_repository = database_repository
        self.notificiation = NotificationRepository('menu')
        self.cache_repository = MenuCacheRepository('menu', 'menus')

    def create(self, menu_data: schemas.MenuCreate | schemas.SubmenuCreate | schemas.DishCreate, **kwargs) -> models.Menu | models.Submenu | models.Dish | None:
        new_menu = self.database_repository.add(menu_data, **kwargs)
        self.cache_repository.deinitialize_all()
        return new_menu

    def delete(self, id, **kwargs) -> dict:
        self.database_repository.delete(id, **kwargs)
        self.cache_repository.deinitialize_all()
        return self.notificiation.delete_success()

    def get_all(self, url_key: str, **kwargs) -> list[models.Menu | models.Submenu | models.Dish | dict | None]:
        cached_response = self.cache_repository.get_all(url_key)
        if cached_response:
            print('cache list hit')
            return cached_response
        all_menus = self.database_repository.get_all(**kwargs)
        self.cache_repository.add_list(url_key, all_menus)
        return all_menus  # type: ignore

    def get(self, url_key: str, **kwargs) -> models.Menu | models.Submenu | models.Dish | dict | None:
        cached_response = self.cache_repository.get(url_key)
        if cached_response:  # if cache exists return cached response
            print('cache hit')
            return cached_response
        menu = self.database_repository.get(
            **kwargs)
        self.cache_repository.add(url_key, menu)
        return menu

    def update(self, menu_data: schemas.MenuCreate | schemas.SubmenuCreate | schemas.DishCreate, id, **kwargs) -> models.Menu | models.Submenu | models.Dish | dict | None:
        update_menu = self.database_repository.update(menu_data, id, **kwargs)
        self.cache_repository.deinitialize_all()
        return update_menu
