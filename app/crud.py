from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from . import models

# Menu Operations


async def get_menu_submenus_count(db: AsyncSession, menu_id: str) -> int:
    query = select(models.Submenu).filter(models.Submenu.menu_id == menu_id)
    result = await db.execute(query)
    return len(result.scalars().all())


async def get_sumbenus_dishes_count(db: AsyncSession, submenu_id: str) -> int:
    query = select(models.Dish).filter(models.Dish.submenu_id == submenu_id)
    result = await db.execute(query)
    return len(result.scalars().all())


async def get_menus_dishes_count(db: AsyncSession, menu_id: str) -> int:
    query = select(models.Dish).join(models.Submenu).filter(models.Submenu.menu_id == menu_id)
    result = await db.execute(query)
    return len(result.scalars().all())
