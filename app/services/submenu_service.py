from typing import Union

from fastapi import Depends

from .. import models, schemas
from ..repositories import (
    DishRepository,
    MenuRepository,
    NotificationRepository,
    SubmenuCacheRepository,
    SubmenuRepository,
)
from .menu_service import MenuService


class SubmenuService(MenuService):
    schema = schemas.SubmenuCreate
    orm_model = models.Submenu
    db_repository = SubmenuRepository

    def __init__(self, database_repository: SubmenuRepository = Depends(), ) -> None:
        self.database_repository = database_repository
        self.notificiation = NotificationRepository('submenu')
        self.cache_repository = SubmenuCacheRepository
