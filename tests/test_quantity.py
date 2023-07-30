import pytest
from sqlalchemy import and_

from app.routers import dishes
from app import schemas
from app import models


### Testing corrent quantity calculations of sub elements in the database


@pytest.mark.parametrize(
    "menu_index",
    (
        (0),
        (1),
    ),
)
def test_submenus_quantitiy_in_menu(
    session, client, PREFIX, test_menus, test_submenus, test_dishes, menu_index
):
    menu_id = test_menus[menu_index].id

    res = client.get(f"{PREFIX}/menus/{menu_id}")
    db_submenus_count = (
        session.query(models.Submenu)
        .join(models.Menu)
        .filter(models.Submenu.menu_id == menu_id)
        .all()
    )

    print(len(db_submenus_count), res.json())
    assert len(db_submenus_count) == res.json()["submenus_count"]


@pytest.mark.parametrize(
    "menu_index",
    (
        (0),
        (1),
    ),
)
def test_dishes_quantitiy_in_menu(
    session, client, PREFIX, test_menus, test_submenus, test_dishes, menu_index
):
    menu_id = test_menus[menu_index].id
    submenu_id = (
        session.query(models.Submenu)
        .filter(models.Submenu.menu_id == menu_id)
        .first()
        .id
    )

    res = client.get(f"{PREFIX}/menus/{menu_id}")
    db_dishes_count = (
        session.query(models.Dish)
        .join(models.Submenu)
        .filter(models.Submenu.menu_id == menu_id)
        .all()
    )
    print(len(db_dishes_count), res.json())
    assert len(db_dishes_count) == res.json()["dishes_count"]


@pytest.mark.parametrize(
    "menu_index",
    (
        (0),
        (1),
    ),
)
def test_dishes_quantitiy_in_submenu(
    session, client, PREFIX, test_menus, test_submenus, test_dishes, menu_index
):
    menu_id = test_menus[menu_index].id
    submenu_id = (
        session.query(models.Submenu)
        .filter(models.Submenu.menu_id == menu_id)
        .first()
        .id
    )

    res = client.get(f"{PREFIX}/menus/{menu_id}/submenus/{submenu_id}")
    db_dishes_count = (
        session.query(models.Dish)
        .join(models.Submenu)
        .filter(
            and_(models.Submenu.id == submenu_id, models.Submenu.menu_id == menu_id)
        )
        .all()
    )

    print(len(db_dishes_count), res.json())
    assert len(db_dishes_count) == res.json()["dishes_count"]
