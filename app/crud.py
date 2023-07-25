from sqlalchemy.orm import Session
from . import utils

from . import models, schemas


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
    return db.query(modles.Menu).filter(modles.Menu.id == id).delete()


def update_menu_by_id(db: Session, menu: schemas.MenuCreate, id: str):
    update_menu = db.query(models.Menu).filter(models.Menu.id == id)
    update_menu.update(menu.dict(), synchronize_session=False)
    # update_menu.title = menu.title
    # update_menu.description = menu.description
    db.commit()
    return update_menu


##################################
##################################
##################################
##################################
##################################
def get_menu_relationship_by_id(db: Session, id: str) -> list[models.Submenu]:
    return db.query(modles.Menu).join(models.Submenu).filter(models.Menu.id == id).all()


def get_submenu_relationship_by_id(db: Session, id: str) -> list[models.Dish]:
    return (
        db.query(modles.Menu).join(models.Submenu).filter(models.Submenu.id == id).all()
    )


def create_submenu(db: Session, menu: schemas.MenuCreate):
    new_submenu = models.Submenu(**menu.dict())
    db.add(new_submenu)
    db.commit()
    db.refresh(new_submenu)
    return new_submenu


def create_dish(db: Session, dish: schemas.DishCreate):
    new_dish = models.Dish(**dish.dict())
    db.add(new_dish)
    db.commit()
    db.refresh(new_dish)
    return new_dish
