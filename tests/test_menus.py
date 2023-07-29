import pytest

from app.routers import menus
from app import schemas
from app import models


# CRUD testing


# Create testing
def test_create_menu(session, client, PREFIX):
    create_data = {
        "title": "test menu 1 title",
        "description": "test menu 1 description",
    }
    res = client.post(f"{PREFIX}/menus", json=create_data)
    print("Test request was sent to", res.url)
    assert res.status_code == 201
    created_menu = schemas.MenuOut(**res.json())
    assert created_menu.title == create_data["title"]
    assert created_menu.description == create_data["description"]


# Read testing
def test_get_menu(session, client, PREFIX, test_menus):
    test_menu_id = test_menus[0].id
    print(session.query(models.Menu).first().created_at)
    res = client.get(f"{PREFIX}/menus/{test_menu_id}")
    print("Test request was sent to", res.url, res.content)
    assert res.status_code == 200
    response_menu = schemas.MenuOut(**res.json())
    assert response_menu.title == test_menus[0].title


# Read multiple testing
def test_read_menus(session, client, PREFIX, test_menus):
    res = client.get(f"{PREFIX}/menus")
    response_data = res.json()
    validated_menus_list = [schemas.MenuOut(**menu) for menu in response_data]

    assert res.status_code == 200
    assert len(validated_menus_list) == len(test_menus)


# Update testing
def test_update_menu(session, client, PREFIX, test_menus):
    test_menu_id = test_menus[0].id
    update_data = {
        "title": "UPDATED test menu 1 title",
        "description": "UPDATED test menu 1 description",
    }
    res = client.patch(f"{PREFIX}/menus/{test_menu_id}", json=update_data)
    print("Test request was sent to", res.url)
    assert res.status_code == 200
    updated_menu = schemas.MenuCreate(**res.json())
    assert updated_menu.title == update_data["title"]
    assert updated_menu.description == update_data["description"]
