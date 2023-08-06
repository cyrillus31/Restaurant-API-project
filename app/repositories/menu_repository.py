# from abc import ABC, abstractclassmethod
# from typing import Any

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from .. import crud, models, schemas
from ..database import get_db

# class AbstractRepository(ABC):
# def __init__(self, *args: Any, **kwargs: Any) -> None:
# raise NotImplementedError

# @abstractclassmethod
# def get(self, *args: Any, **kwargs: Any):
# raise NotImplementedError

# @abstractclassmethod
# def get_all(self, *args: Any, **kwargs: Any):
# raise NotImplementedError

# @abstractclassmethod
# def add(self, *args: Any, **kwargs: Any):
# raise NotImplementedError

# @abstractclassmethod
# def update(self, *args: Any, **kwargs: Any):
# raise NotImplementedError

# @abstractclassmethod
# def delete(self, id: str, **kwargs) -> None:
# raise NotImplementedError


# class MenuRepository(AbstractRepository):
class MenuRepository():
    orm_model = models.Menu
    schema = schemas.MenuCreate

    def __init__(self, db: Session = Depends(get_db)) -> None:
        self.db = db
        self.orm_model = models.Menu
        self.detail_404 = 'menu not found'
        self.detail_400 = 'Menu with this title already exists'

    def get_all(self, skip: int = 0, limit: int = 100, **kwargs) -> list[models.Menu | models.Submenu | models.Dish | None]:
        menus = self.db.query(self.orm_model).filter_by(**kwargs).offset(
            skip).limit(limit).all()

        # count submenus and dishes
        for db_menu in menus:
            db_menu.submenus_count = crud.get_menu_submenus_count(
                self.db, db_menu.id)
            db_menu.dishes_count = crud.get_menus_dishes_count(
                self.db, db_menu.id)
        return menus

    def get(self, **kwargs):
        menu = self.db.query(
            self.orm_model).filter_by(**kwargs).first()
        if not menu:
            raise HTTPException(
                status_code=404, detail=f'{self.detail_404}')

        # count submenus and dishes
        menu.submenus_count = crud.get_menu_submenus_count(self.db, menu.id)
        menu.dishes_count = crud.get_menus_dishes_count(self.db, menu.id)
        return menu

    def add(self, menu: schemas.MenuCreate | schemas.SubmenuCreate | schemas.DishCreate, **kwargs) -> models.Menu | models.Submenu | models.Dish | None:
        menu_exists = self.db.query(self.orm_model).filter(
            self.orm_model.title == menu.title).filter_by(**kwargs).first()
        if menu_exists:
            raise HTTPException(
                status_code=400, detail=f'{self.detail_400}'
            )
        new_menu = self.orm_model(**menu.dict(), **kwargs)
        self.db.add(new_menu)
        self.db.commit()
        self.db.refresh(new_menu)
        return new_menu

    def delete(self, id: str, **kwargs) -> None:
        menu_exists = self.get(id=id, **kwargs)
        if not menu_exists:
            raise HTTPException(
                status_code=404, detail=f'{self.detail_404}')
        self.db.query(self.orm_model).filter(
            self.orm_model.id == id).delete()
        self.db.commit()

    def update(self, menu: schemas.MenuCreate | schemas.SubmenuCreate | schemas.DishCreate, id: str, **kwargs) -> models.Menu | models.Submenu | models.Dish | None:
        # menu_exists = self.get(id=id)
        menu_exists = self.db.query(self.orm_model).filter(
            self.orm_model.id == id).filter_by(**kwargs).first()
        if not menu_exists:
            raise HTTPException(
                status_code=404, detail=f'{self.detail_404}')

        update_menu = self.db.query(
            self.orm_model).filter(self.orm_model.id == id)
        update_menu.update(menu.dict(), synchronize_session=False)
        self.db.commit()
        return update_menu.first()
