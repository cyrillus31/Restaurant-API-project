from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from .. import crud, models
from ..database import get_db
from .menu_repository import MenuRepository


class SubmenuRepository(MenuRepository):

    def __init__(self, db: Session = Depends(get_db)) -> None:
        self.db = db
        self.orm_model = models.Submenu
        self.detail_404 = 'submenu not found'
        self.detail_400 = 'Submenu with this title already exists'

    def get_all(self, skip: int = 0, limit: int = 100, **kwargs) -> list[models.Menu | models.Submenu | models.Dish | None]:
        menus = self.db.query(self.orm_model).filter_by(**kwargs).offset(
            skip).limit(limit).all()

        # count submenus and dishes
        for db_menu in menus:
            db_menu.dishes_count = crud.get_sumbenus_dishes_count(
                self.db, db_menu.id)
        return menus

    def get(self, **kwargs):
        menu = self.db.query(
            self.orm_model).filter_by(**kwargs).first()
        if not menu:
            raise HTTPException(
                status_code=404, detail=f'{self.detail_404}')

        # count submenus and dishes
        menu.dishes_count = crud.get_sumbenus_dishes_count(self.db, menu.id)
        return menu
