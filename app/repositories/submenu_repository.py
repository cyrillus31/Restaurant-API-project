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


class SubmenuRepository(AbstractRepository):
    def __init__(self, db: Session = Depends(get_db)) -> None:
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100) -> list[models.Menu]:
        menus = self.db.query(models.Menu).offset(skip).limit(limit).all()

        # count submenus and dishes
        for db_menu in menus:
            db_menu.submenus_count = crud.get_menu_submenus_count(
                self.db, db_menu.id)
            db_menu.dishes_count = crud.get_menus_dishes_count(
                self.db, db_menu.id)
        return menus

    def get(self, **kwargs):
        menu = self.db.query(models.Menu).filter_by(**kwargs).first()
        if not menu:
            raise HTTPException(status_code=404, detail="menu not found")

        # count submenus and dishes
        menu.submenus_count = crud.get_menu_submenus_count(self.db, menu.id)
        menu.dishes_count = crud.get_menus_dishes_count(self.db, menu.id)
        return menu

    def add(self, menu_id, submenu: schemas.MenuCreate) -> models.Menu:
        submenu_exists = self.db.query(models.Submenu).filter(
            models.Menu.title == menu.title).first()
        if submenu_exists:
            raise HTTPException(
                status_code=400, detail="Menu with this title already exists"
            )
        new_menu = models.Menu(**menu.dict())
        self.db.add(new_menu)
        self.db.commit()
        self.db.refresh(new_menu)
        return new_menu

    def delete(self, id: str) -> None:
        menu_exists = self.get(id=id)
        if not menu_exists:
            raise HTTPException(status_code=404, detail="menu not found")
        self.db.query(models.Menu).filter(models.Menu.id == id).delete()
        self.db.commit()

    def update(self, menu: schemas.MenuCreate, id: str) -> models.Menu:
        # menu_exists = self.get(id=id)
        menu_exists = self.db.query(models.Menu).filter(
            models.Menu.id == id).first()
        if not menu_exists:
            raise HTTPException(status_code=404, detail="menu not found")

        update_menu = self.db.query(
            models.Menu).filter(models.Menu.id == id)
        update_menu.update(menu.dict(), synchronize_session=False)
        self.db.commit()
        return update_menu.first()


####### Menu Operations ############

def create_menu(db: Session, menu: schemas.MenuCreate):
    new_menu = models.Menu(**menu.dict())
    db.add(new_menu)
    db.commit()

    db.refresh(new_menu)

    return new_menu


def get_menus(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Menu).offset(skip).limit(limit).all()


def get_menu_by_title(db: Session, title: str):
    return db.query(models.Menu).filter(models.Menu.title == title).first()


def get_menu_by_id(db: Session, id: str):
    return db.query(models.Menu).filter(models.Menu.id == id).first()


def delete_menu_by_id(db: Session, id: str):
    db.query(models.Menu).filter(models.Menu.id == id).delete()

    db.commit()


def update_menu_by_id(db: Session, menu: schemas.MenuCreate, id: str):
    update_menu = db.query(models.Menu).filter(models.Menu.id == id)

    update_menu.update(menu.dict(), synchronize_session=False)

    db.commit()

    return update_menu.first()


####### Submenu operations########


def create_submenu(menu_id, db: Session, submenu: schemas.MenuCreate):
    new_submenu = models.Submenu(
        title=submenu.title,
        description=submenu.description,
        menu_id=menu_id,
    )

    db.add(new_submenu)

    db.commit()

    db.refresh(new_submenu)

    return new_submenu


def get_submenus(menu_id, db: Session, skip: int = 0, limit: int = 100):
    return (
        db.query(models.Submenu)
        .filter(models.Submenu.menu_id == menu_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_submenu_by_title(db: Session, title: str):
    # search only by title fix later

    return db.query(models.Submenu).filter(models.Submenu.title == title).first()


def get_submenu_by_id(db: Session, id: str):
    return db.query(models.Submenu).filter(models.Submenu.id == id).first()


def delete_submenu_by_id(db: Session, id: str):
    db.query(models.Submenu).filter(models.Submenu.id == id).delete()

    db.commit()


def update_submenu_by_id(db: Session, submenu: schemas.MenuCreate, id: str):
    update_menu = db.query(models.Submenu).filter(models.Submenu.id == id)

    update_menu.update(submenu.dict(), synchronize_session=False)

    db.commit()

    return update_menu.first()


####### Dishes operations ########


def create_dish(submenu_id, db: Session, dish: schemas.MenuCreate):
    new_dish = models.Dish(
        title=dish.title,
        description=dish.description,
        submenu_id=submenu_id,
        price=dish.price,
    )

    db.add(new_dish)
    db.commit()
    db.refresh(new_dish)

    return new_dish


def get_dishes(submenu_id, db: Session, skip: int = 0, limit: int = 100):
    return (
        db.query(models.Dish)
        .filter(models.Dish.submenu_id == submenu_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_dish_by_title(db: Session, title: str):
    return db.query(models.Dish).filter(models.Dish.title == title).first()


def get_dish_by_id(db: Session, id: str):
    return db.query(models.Dish).filter(models.Dish.id == id).first()


def delete_dish_by_id(db: Session, id: str):
    db.query(models.Dish).filter(models.Dish.id == id).delete()

    db.commit()


def update_dish_by_id(db: Session, dish: schemas.DishCreate, id: str):
    update_dish = db.query(models.Dish).filter(models.Dish.id == id)

    update_dish.update(dish.dict(), synchronize_session=False)

    db.commit()

    return update_dish.first()


def get_menu_submenus_count(db, menu_id):
    return len(db.query(models.Submenu).filter(models.Submenu.menu_id == menu_id).all())


def get_sumbenus_dishes_count(db, submenu_id):
    return len(db.query(models.Dish).filter(models.Dish.submenu_id == submenu_id).all())


def get_menus_dishes_count(db, menu_id):
    return len(
        db.query(models.Dish)
        .join(models.Submenu)
        .filter(models.Submenu.menu_id == menu_id)
        .all()
    )
