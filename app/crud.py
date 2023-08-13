from sqlalchemy import select
from sqlalchemy.orm import Session

from . import models, schemas

# Menu Operations


async def get_menu_submenus_count(db, menu_id):
    # return len(db.query(models.Submenu).filter(models.Submenu.menu_id == menu_id).all())
    query = select(models.Submenu).filter(models.Submenu.menu_id == menu_id)
    result = await db.execute(query)
    return len(result.scalars().all())


async def get_sumbenus_dishes_count(db, submenu_id):
    # return len(db.query(models.Dish).filter(models.Dish.submenu_id == submenu_id).all())
    query = select(models.Dish).filter(models.Dish.submenu_id == submenu_id)
    result = await db.execute(query)
    return len(result.scalars().all())


async def get_menus_dishes_count(db, menu_id):
    # return len(db.query(models.Dish).join(models.Submenu).filter(models.Submenu.menu_id == menu_id).all())
    query = select(models.Dish).join(models.Submenu).filter(models.Submenu.menu_id == menu_id)
    result = await db.execute(query)
    return len(result.scalars().all())
