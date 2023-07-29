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
    created_menu = schemas.MenuCreate(**res.json())
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


# Read
