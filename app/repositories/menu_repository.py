from abc import ABC, abstractclassmethod
from typing import Union

from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status

from .. import models, schemas
from ..database import get_db
from .. import crud


class AbstractRepository(ABC):
    @abstractclassmethod
    def get(self): ...

    @abstractclassmethod
    def get_all(self): ...

    @abstractclassmethod
    def add(self): ...

    @abstractclassmethod
    def update(self): ...

    @abstractclassmethod
    def delete(self): ...


class MenuRepository(AbstractRepository):
    orm_model = models.Menu
    schema = schemas.MenuCreate
    detail_404 = "menu not found"
    detail_400 = "Menu with this title already exists"

    def __init__(self, db: Session = Depends(get_db)) -> None:
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100) -> list[orm_model]:
        menus = self.db.query(MenuRepository.orm_model).offset(
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
            MenuRepository.orm_model).filter_by(**kwargs).first()
        if not menu:
            raise HTTPException(
                status_code=404, detail=f"{MenuRepository.detail_404}")

        # count submenus and dishes
        menu.submenus_count = crud.get_menu_submenus_count(self.db, menu.id)
        menu.dishes_count = crud.get_menus_dishes_count(self.db, menu.id)
        return menu

    def add(self, menu: schema, **kwargs) -> orm_model:
        menu_exists = self.db.query(MenuRepository.orm_model).filter(
            MenuRepository.orm_model.title == menu.title).filter_by(**kwargs).first()
        if menu_exists:
            raise HTTPException(
                status_code=400, detail=f"{MenuRepository.detail_400}"
            )
        new_menu = MenuRepository.orm_model(**menu.dict(), **kwargs)
        self.db.add(new_menu)
        self.db.commit()
        self.db.refresh(new_menu)
        return new_menu

    def delete(self, id: str, **kwargs) -> None:
        menu_exists = self.get(id=id, **kwargs)
        if not menu_exists:
            raise HTTPException(
                status_code=404, detail=f"{MenuRepository.detail_404}")
        self.db.query(MenuRepository.orm_model).filter(
            MenuRepository.orm_model.id == id).delete()
        self.db.commit()

    def update(self, menu: schema, id: str, **kwargs) -> orm_model:
        # menu_exists = self.get(id=id)
        menu_exists = self.db.query(MenuRepository.orm_model).filter(
            MenuRepository.orm_model.id == id).filter_by(**kwargs).first()
        if not menu_exists:
            raise HTTPException(
                status_code=404, detail=f"{MenuRepository.detail_404}")

        update_menu = self.db.query(
            MenuRepository.orm_model).filter(MenuRepository.orm_model.id == id)
        update_menu.update(menu.dict(), synchronize_session=False)
        self.db.commit()
        return update_menu.first()
