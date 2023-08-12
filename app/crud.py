# from sqlalchemy.orm import Session
from databases import Database

from . import models, schemas

# Menu Operations


async def create_menu(db: Database, menu: schemas.MenuCreate):
    new_menu = models.Menu(**menu.dict())
    await db.add(new_menu)
    await db.commit()
    await db.refresh(new_menu)
    return new_menu


async def get_menus(db: Database, skip: int = 0, limit: int = 100):
    return await db.query(models.Menu).offset(skip).limit(limit).all()


async def get_menu_by_title(db: Database, title: str):
    return await db.query(models.Menu).filter(models.Menu.title == title).first()


async def get_menu_by_id(db: Database, id: str):
    return await db.query(models.Menu).filter(models.Menu.id == id).first()


async def delete_menu_by_id(db: Database, id: str):
    await db.query(models.Menu).filter(models.Menu.id == id).delete()

    await db.commit()


async def update_menu_by_id(db: Database, menu: schemas.MenuCreate, id: str):
    update_menu = await db.query(models.Menu).filter(models.Menu.id == id)

    update_menu.update(menu.dict(), synchronize_session=False)

    await db.commit()

    return update_menu.first()


# Submenu operations


async def create_submenu(menu_id, db: Database, submenu: schemas.MenuCreate):
    new_submenu = models.Submenu(
        title=submenu.title,
        description=submenu.description,
        menu_id=menu_id,
    )

    await db.add(new_submenu)
    await db.commit()
    await db.refresh(new_submenu)

    return new_submenu


async def get_submenus(menu_id, db: Database, skip: int = 0, limit: int = 100):
    return (
        await db.query(models.Submenu)
        .filter(models.Submenu.menu_id == menu_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


async def get_submenu_by_title(db: Database, title: str):
    # search only by title fix later

    return await db.query(models.Submenu).filter(models.Submenu.title == title).first()


async def get_submenu_by_id(db: Database, id: str):
    return await db.query(models.Submenu).filter(models.Submenu.id == id).first()


async def delete_submenu_by_id(db: Database, id: str):
    await db.query(models.Submenu).filter(models.Submenu.id == id).delete()

    await db.commit()


async def update_submenu_by_id(db: Database, submenu: schemas.MenuCreate, id: str):
    update_menu = await db.query(models.Submenu).filter(models.Submenu.id == id)

    update_menu.update(submenu.dict(), synchronize_session=False)

    await db.commit()

    return update_menu.first()


# Dishes operations


async def create_dish(submenu_id, db: Database, dish: schemas.MenuCreate):
    new_dish = models.Dish(
        title=dish.title,
        description=dish.description,
        submenu_id=submenu_id,
        price=dish.price,
    )

    await db.add(new_dish)
    await db.commit()
    await db.refresh(new_dish)

    return new_dish


async def get_dishes(submenu_id, db: Database, skip: int = 0, limit: int = 100):
    return (
        await db.query(models.Dish)
        .filter(models.Dish.submenu_id == submenu_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


async def get_dish_by_title(db: Database, title: str):
    return await db.query(models.Dish).filter(models.Dish.title == title).first()


async def get_dish_by_id(db: Database, id: str):
    return await db.query(models.Dish).filter(models.Dish.id == id).first()


async def delete_dish_by_id(db: Database, id: str):
    await db.query(models.Dish).filter(models.Dish.id == id).delete()
    await db.commit()


async def update_dish_by_id(db: Database, dish: schemas.DishCreate, id: str):
    update_dish = await db.query(models.Dish).filter(models.Dish.id == id)
    await update_dish.update(dish.dict(), synchronize_session=False)
    await db.commit()
    return update_dish.first()


async def get_menu_submenus_count(db, menu_id):
    return len(await db.query(models.Submenu).filter(models.Submenu.menu_id == menu_id).all())


async def get_sumbenus_dishes_count(db, submenu_id):
    return len(await db.query(models.Dish).filter(models.Dish.submenu_id == submenu_id).all())


async def get_menus_dishes_count(db, menu_id):
    return len(
        await db.query(models.Dish)
        .join(models.Submenu)
        .filter(models.Submenu.menu_id == menu_id)
        .all()
    )
