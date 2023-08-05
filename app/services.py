from fastapi import Depends

from .repositories import MenuRepository, NotificationRepository
from . import schemas
from . import models


class MenuService:
    def __init__(self, database_repository: MenuRepository = Depends()):
        self.database_repository = database_repository
        self.notificiation = NotificationRepository

    def create(self, menu_data: schemas.MenuCreate) -> models.Menu:
        new_menu = self.database_repository.add(menu_data)
        return new_menu

    def delete(self, id) -> None:
        self.database_repository.delete(id)
        return self.notificiation.delete_success()

    def get_all(self, **kwargs) -> list[models.Menu]:
        all_menus = self.database_repository.get_all(**kwargs)
        return all_menus

    def get(self, **kwargs) -> models.Menu:
        return self.database_repository.get(**kwargs)

    def update(self, menu_data, id) -> models.Menu:
        return self.database_repository.update(menu_data, id)
