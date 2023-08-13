from sqlalchemy import select

from app import models, schemas


# CRUD testing
async def submenu_id_search(session, menu_id) -> int:
    result = (
        await session.execute(select(models.Submenu).filter(models.Submenu.menu_id == menu_id))
    )
    submenu_id = result.scalars().first().id
    return submenu_id


async def dish_id_search(session, submenu_id) -> int:
    result = (
        await session.execute(select(models.Dish).filter(models.Dish.submenu_id == submenu_id))
    )
    dish_id = result.scalars().first().id
    return dish_id


# Create testing
async def test_create_dish(session, client, PREFIX, test_menus, test_submenus):
    menu_id = test_menus[0].id
    result = (
        await session.execute(select(models.Submenu).filter(models.Submenu.menu_id == menu_id))
    )
    submenu_id = result.scalars().first().id
    create_data = {
        'title': 'test submenu 1 title',
        'description': 'test submenu 1 description',
        'price': '111.10',
    }
    res = await client.post(
        f'{PREFIX}/menus/{menu_id}/submenus/{submenu_id}/dishes/', json=create_data
    )
    print('Test request was sent to', res.url)
    assert res.status_code == 201
    created_menu = schemas.DishOut(**res.json())
    assert created_menu.title == create_data['title']
    assert created_menu.description == create_data['description']
    assert created_menu.price == create_data['price']


# Read testing
async def test_get_dish(session, client, PREFIX, test_menus, test_submenus, test_dishes):
    menu_id = test_menus[0].id
    submenu_id = await submenu_id_search(session, menu_id)
    dish_id = await dish_id_search(session, submenu_id)
    res = await client.get(
        f'{PREFIX}/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
    print('Test request was sent to', res.url)
    assert res.status_code == 200
    response_submenu = schemas.DishOut(**res.json())
    result = await session.execute(select(models.Dish).filter(models.Dish.id == dish_id))
    db_dish = result.scalars().first()
    assert response_submenu.title == db_dish.title
    assert response_submenu.description == db_dish.description
    assert response_submenu.price == db_dish.price


async def test_get_menu_not_exists(
    session, client, PREFIX, test_menus, test_submenus, test_dishes
):
    menu_id = test_menus[0].id
    submenu_id = await submenu_id_search(session, menu_id)

    res = await client.get(
        f'{PREFIX}/menus/{menu_id}/submenus/{submenu_id}/dishes/9876543210'
    )
    assert res.status_code == 404
    assert res.json()['detail'] == 'dish not found'


# Read multiple testing
async def test_read_dishes(session, client, PREFIX, test_menus, test_submenus, test_dishes):
    menu_id = test_menus[0].id
    result = (
        await session.execute(select(models.Submenu).filter(models.Submenu.menu_id == menu_id))
    )
    submenu_id = result.scalars().first().id
    res = await client.get(f'{PREFIX}/menus/{menu_id}/submenus/{submenu_id}/dishes/')
    response_data = res.json()
    validated_dishes_list = [schemas.DishOut(**dish) for dish in response_data]
    result = (
        await session.execute(select(models.Dish).filter(
            models.Dish.submenu_id == submenu_id))
    )
    dishes_of_submenu_list = result.scalars().all()

    assert res.status_code == 200
    assert len(validated_dishes_list) == len(dishes_of_submenu_list)


async def test_read_menus_empty(session, client, PREFIX, test_menus, test_submenus):
    menu_id = test_menus[0].id
    result = (
        await session.execute(select(models.Submenu).filter(models.Submenu.menu_id == menu_id))
    )
    submenu_id = result.scalars().first().id
    res = await client.get(f'{PREFIX}/menus/{menu_id}/submenus/{submenu_id}/dishes/')
    assert res.status_code == 200
    assert res.json() == []


# Update testing
async def test_update_dish(session, client, PREFIX, test_menus, test_submenus, test_dishes):
    menu_id = test_menus[0].id
    submenu_id = await submenu_id_search(session, menu_id)
    dish_id = await dish_id_search(session, submenu_id)

    update_data = {
        'title': 'UPDATED test dish title',
        'description': 'UPDATED test dish description',
        'price': '123.00',
        # "submenu_id": submenu_id,
    }
    res = await client.patch(
        f'{PREFIX}/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
        json=update_data,
    )
    print('Test request was sent to', res.url)
    assert res.status_code == 200
    updated_menu = schemas.DishOut(**res.json())
    assert updated_menu.title == update_data['title']
    assert updated_menu.description == update_data['description']
    assert updated_menu.price == update_data['price']


async def test_update_menu_not_exists(
    session, client, PREFIX, test_menus, test_submenus, test_dishes
):
    menu_id = test_menus[0].id
    submenu_id = await submenu_id_search(session, menu_id)
    update_data = {
        'title': 'UPDATED test dish title',
        'description': 'UPDATED test dish description',
        'price': '321.98'
        # "submenu_id": 9876543210,
    }
    res = await client.patch(
        f'{PREFIX}/menus/{menu_id}/submenus/{submenu_id}/dishes/9876543210',
        json=update_data,
    )
    assert res.status_code == 404
    assert res.json()['detail'] == 'dish not found'


# Delete testing
async def test_delete_dish(session, client, PREFIX, test_menus, test_submenus, test_dishes):
    menu_id = test_menus[0].id
    submenu_id = await submenu_id_search(session, menu_id)
    dish_id = await dish_id_search(session, submenu_id)

    res = await client.delete(
        f'{PREFIX}/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}'
    )
    print('Test request was sent to', res.url)
    assert res.status_code == 200
    assert res.json()['status'] is True
    assert res.json()['message'] == 'The dish has been deleted'

    result = await session.execute(select(models.Dish))
    all_dishes_list = result.scalars().all()
    assert len(all_dishes_list) == len(test_dishes) - 1


async def test_delete_dish_not_exists(
    session, client, PREFIX, test_menus, test_submenus, test_dishes
):
    menu_id = test_menus[0].id
    submenu_id = await submenu_id_search(session, menu_id)
    res = await client.delete(
        f'{PREFIX}/menus/{menu_id}/submenus/{submenu_id}/dishes/9876543210'
    )
    assert res.status_code == 404
    assert res.json()['detail'] == 'dish not found'
