from fastapi import Depends

from .. import models, schemas
from ..repositories import DishCacheRepository, DishRepository, NotificationRepository
from .menu_service import MenuService


class DishService(MenuService):
    schema = schemas.DishCreate
    orm_model = models.Dish
    db_repository = DishRepository

    def __init__(self, database_repository: DishRepository = Depends(), ) -> None:
        self.database_repository = database_repository
        self.notificiation = NotificationRepository('dish')
        self.cache_repository = DishCacheRepository('dish', 'dishes')
