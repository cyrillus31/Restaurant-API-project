import pytest

from app.routers import menus
from app import schemas


def test_create_post(session, client):
    create_data = {
        "title": "test menu 1 title",
        "description": "test menu 1 description",
    }
    res = client.post(f"{prefix}/menus", json=create_data)
    assert res.status_code == 201
    created_user = schemas.UserCreate(**res.json())
    assert created_user.title == create_data["title"]
    assert created_user.description == create_data["description"]
