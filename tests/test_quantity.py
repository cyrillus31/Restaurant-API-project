import pytest
from httpx import AsyncClient
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app import models

# Testing corrent quantity calculations of sub elements in the database


@pytest.mark.parametrize(
    'menu_index',
    (
        (0),
        (1),
    ),
)
async def test_submenus_quantitiy_in_menu(
    session: AsyncSession, client: AsyncClient, PREFIX: str, test_menus: list[models.Menu], test_submenus: list[models.Submenu], test_dishes: list[models.Dish], menu_index: int
) -> None:
    menu_id = test_menus[menu_index].id

    res = await client.get(f'{PREFIX}/menus/{menu_id}')
    result = (
        await session.execute(select(models.Submenu)
                              .join(models.Menu)
                              .filter(models.Submenu.menu_id == menu_id))
    )
    db_submenus_count = result.scalars().all()
    print(len(db_submenus_count), res.json())
    assert len(db_submenus_count) == res.json()['submenus_count']


@pytest.mark.parametrize(
    'menu_index',
    (
        (0),
        (1),
    ),
)
async def test_dishes_quantitiy_in_menu(
    session: AsyncSession, client: AsyncClient, PREFIX: str, test_menus: list[models.Menu], test_submenus: list[models.Submenu], test_dishes: list[models.Dish], menu_index: int
) -> None:
    menu_id = test_menus[menu_index].id

    res = await client.get(f'{PREFIX}/menus/{menu_id}')
    result = (
        await session.execute(select(models.Dish)
                              .join(models.Submenu)
                              .filter(models.Submenu.menu_id == menu_id))
    )
    db_dishes_count = result.scalars().all()
    print(len(db_dishes_count), res.json())
    assert len(db_dishes_count) == res.json()['dishes_count']


@pytest.mark.parametrize(
    'menu_index',
    (
        (0),
        (1),
    ),
)
async def test_dishes_quantitiy_in_submenu(
    session: AsyncSession, client: AsyncClient, PREFIX: str, test_menus: list[models.Menu], test_submenus: list[models.Submenu], test_dishes: list[models.Dish], menu_index: int
) -> None:
    menu_id = test_menus[menu_index].id
    result = (
        await session.execute(select(models.Submenu)
                              .filter(models.Submenu.menu_id == menu_id))
    )
    submenu_id = result.scalars().first().id

    res = await client.get(f'{PREFIX}/menus/{menu_id}/submenus/{submenu_id}')
    result = (
        await session.execute(select(models.Dish)
                              .join(models.Submenu)
                              .filter(
            and_(models.Submenu.id == submenu_id,
                 models.Submenu.menu_id == menu_id)))
    )
    db_dishes_count = result.scalars().all()

    print(len(db_dishes_count), res.json())
    assert len(db_dishes_count) == res.json()['dishes_count']
