import pytest

from app.routers import dishes
from app import schemas
from app import models

### CRUD testing


# Create testing
def test_create_dish(session, client, PREFIX, test_menus, test_submenus):
    menu_id = test_menus[0].id
    submenu_id = (
        session.query(models.Submenu)
        .filter(models.Submenu.menu_id == menu_id)
        .first()
        .id
    )

    create_data = {
        "title": "test submenu 1 title",
        "description": "test submenu 1 description",
        "price": "111.10",
    }
    res = client.post(
        f"{PREFIX}/menus/{menu_id}/submenus/{submenu_id}/dishes", json=create_data
    )
    print("Test request was sent to", res.url)
    assert res.status_code == 201
    created_menu = schemas.DishOut(**res.json())
    assert created_menu.title == create_data["title"]
    assert created_menu.description == create_data["description"]
    assert created_menu.price == create_data["price"]


# Read testing
def test_get_submenu(session, client, PREFIX, test_menus, test_submenus, test_dishes):
    menu_id = test_menus[0].id
    submenu_id = (
        session.query(models.Submenu)
        .filter(models.Submenu.menu_id == menu_id)
        .first()
        .id
    )
    dish_id = (
        session.query(models.Dish).filter(models.Dish.submenu_id == menu_id).first().id
    )
    res = client.get(f"{PREFIX}/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
    print("Test request was sent to", res.url)
    assert res.status_code == 200
    response_submenu = schemas.DishOut(**res.json())
    db_dish = session.query(models.Dish).filter(models.Dish.id == dish_id)
    assert response_submenu.title == db_dish.title
    assert response_submenu.description == db_dish.description
    assert response_submenu.price == db_dish.price


def test_get_menu_not_exists(
    session, client, PREFIX, test_menus, test_submenus, test_dishes
):
    menu_id = test_menus[0].id
    submenu_id = (
        session.query(models.Submenu)
        .filter(models.Submenu.menu_id == menu_id)
        .first()
        .id
    )
    res = client.get(
        f"{PREFIX}/menus/{menu_id}/submenus/{submenu_id}/dishes/9876543210"
    )
    assert res.status_code == 404
    assert res.json()["detail"] == "dish not found"
