from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from .menu_repository import MenuRepository


class DishRepository(MenuRepository):
    orm_model = models.Dish
    schema = schemas.DishCreate

    def __init__(self, db: Session = Depends(get_db)) -> None:
        self.db = db
        self.orm_model = models.Dish
        self.detail_404 = 'dish not found'
        self.detail_400 = 'Dish with this title already exists'

    def get_all(self, skip: int = 0, limit: int = 100, **kwargs) -> list[orm_model]:
        menus = self.db.query(self.orm_model).filter_by(**kwargs).offset(
            skip).limit(limit).all()
        return menus

    def get(self, **kwargs):
        menu = self.db.query(
            self.orm_model).filter_by(**kwargs).first()
        if not menu:
            raise HTTPException(
                status_code=404, detail=f'{self.detail_404}')
        return menu
