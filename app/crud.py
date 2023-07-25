from sqlalchemy.orm import Session


from . import models, schemas


#######Menu Operations############


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


#######Submenu operations########


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


#######Dishes operations ########


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
