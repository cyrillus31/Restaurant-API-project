import pytest
from sqlalchemy import and_, select

from app import models

"""
#######################################

TEST DATABASE STRUCTURE using fixtures

Restaurant
├── Menu 1
│   ├── Submenu 1
│   │   ├── Dish 1
│   │   └── Dish 2
│   └── Submenu 2
│       └── Dish 3
├── Menu 2
│   └── Submenu 3
└── Menu 3

#######################################

"""


async def test_getall_endpoint(
    session, client, PREFIX, test_menus, test_submenus, test_dishes,
):
    res = await client.get(f'{PREFIX}/getall/')
    list_of_menus = res.json()['all menus']
    list_of_submenus_of_first_menu = res.json()['all menus'][0]['submenus']
    list_of_dishes_of_first_submenu = res.json()['all menus'][0]['submenus'][0]['dishes']
    list_of_submenus_of_second_menu = res.json()['all menus'][1]['submenus']
    list_of_submenus_of_third_menu = res.json()['all menus'][2]['submenus']

    assert len(list_of_menus) == 3
    assert len(list_of_submenus_of_first_menu) == 2
    assert len(list_of_dishes_of_first_submenu) == 2
    assert len(list_of_submenus_of_second_menu) == 1
    assert len(list_of_submenus_of_third_menu) == 0
