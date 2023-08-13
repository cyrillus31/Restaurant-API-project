from fastapi import Depends, BackgroundTasks

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

    async def create(self, url_key: str, menu_data: schemas.MenuCreate | schemas.SubmenuCreate | schemas.DishCreate, background_tasks: BackgroundTasks, **kwargs) -> models.Menu | models.Submenu | models.Dish | None:
        new_menu = await self.database_repository.add(menu_data, **kwargs)
        background_tasks.add_task(self.cache_repository.invalidate_all_related_cache, url_key)
        return new_menu

    async def delete(self, url_key: str, id: str, background_tasks: BackgroundTasks, **kwargs) -> dict:
        await self.database_repository.delete(id, **kwargs)
        background_tasks.add_task(self.cache_repository.invalidate_all_related_cache, url_key)
        return self.notificiation.delete_success()

    async def get_all(self, url_key: str, **kwargs) -> list[models.Menu | models.Submenu | models.Dish | dict | None]:
        cached_response = self.cache_repository.get_all(url_key)

        if cached_response:
            print('cache list hit')
            return cached_response

        all_menus = await self.database_repository.get_all(**kwargs)
        self.cache_repository.add_list(url_key, all_menus)

        return all_menus  # type: ignore

    async def get(self, url_key: str, **kwargs) -> models.Menu | models.Submenu | models.Dish | dict | None:
        cached_response = self.cache_repository.get(url_key)
        if cached_response:  # if cache exists return cached response
            print('cache hit')
            return cached_response

        menu = await self.database_repository.get(**kwargs)

        self.cache_repository.add(url_key, menu)
        return menu

    async def update(self, menu_data: schemas.MenuCreate | schemas.SubmenuCreate | schemas.DishCreate, id, background_tasks: BackgroundTasks, **kwargs) -> models.Menu | models.Submenu | models.Dish | dict | None:
        update_menu = await self.database_repository.update(menu_data, id, **kwargs)
        background_tasks.add_task(self.cache_repository.invalidate_update_cache, id)
        return update_menu
