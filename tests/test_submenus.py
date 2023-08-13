from sqlalchemy import select

from app import models, schemas

# CRUD testing

# async def filter_query(session, orm_model, **kwargs) -> list:
    # query = select(orm_model).filter_by(**kwargs)
    # result = await session.execute(query)
    # return result.scalars().all()

# Create testing
async def test_create_menu(session, client, PREFIX, test_menus):
    menu_id = test_menus[0].id
    create_data = {
        'title': 'test submenu 1 title',
        'description': 'test submenu 1 description',
    }
    res = await client.post(f'{PREFIX}/menus/{menu_id}/submenus/', json=create_data)
    print('Test request was sent to', res.url)
    assert res.status_code == 201
    created_menu = schemas.SubmenuOut(**res.json())
    assert created_menu.title == create_data['title']
    assert created_menu.description == create_data['description']


# Read testing
async def test_get_submenu(session, client, PREFIX, test_menus, test_submenus):
    menu_id = test_menus[0].id
    result = (
        await session.execute(select(models.Submenu).filter(models.Submenu.menu_id == menu_id))
    )
    submenu_id = result.scalars().first().id
    res = await client.get(f'{PREFIX}/menus/{menu_id}/submenus/{submenu_id}')
    print('Test request was sent to', res.url)
    assert res.status_code == 200
    response_submenu = schemas.SubmenuOut(**res.json())
    result = (
        await session.execute(select(models.Submenu).filter(models.Submenu.id == submenu_id))
    )
    db_submenu = result.scalars().first()
    assert response_submenu.title == db_submenu.title
    assert response_submenu.description == db_submenu.description


async def test_get_menu_not_exists(session, client, PREFIX, test_menus, test_submenus):
    menu_id = test_menus[0].id
    res = await client.get(f'{PREFIX}/menus/{menu_id}/submenus/987654321')
    assert res.status_code == 404
    assert res.json()['detail'] == 'submenu not found'


# Read multiple testing
async def test_read_submenus(session, client, PREFIX, test_menus, test_submenus):
    menu_id = test_menus[0].id
    res = await client.get(f'{PREFIX}/menus/{menu_id}/submenus/')
    response_data = res.json()
    validated_submenus_list = [
        schemas.SubmenuOut(**submenu) for submenu in response_data
    ]
    result = (
        await session.execute(select(models.Submenu).filter(
            models.Submenu.menu_id == menu_id))
    )
    submenus_of_menu_list = result.scalars().all()

    assert res.status_code == 200
    assert len(validated_submenus_list) == len(submenus_of_menu_list)


async def test_read_menus_empty(session, client, PREFIX, test_menus):
    menu_id = test_menus[0].id
    res = await client.get(f'{PREFIX}/menus/{menu_id}/submenus/')
    assert res.status_code == 200
    assert res.json() == []


# Update testing
async def test_update_menu(session, client, PREFIX, test_menus, test_submenus):
    menu_id = test_menus[0].id
    result = (
        await session.execute(select(models.Submenu).filter(models.Submenu.menu_id == menu_id))
    )
    submenu_id = result.scalars().first().id

    update_data = {
        'title': 'UPDATED test submenu title',
        'description': 'UPDATED test submenu description',
        'menu_id': menu_id,
    }
    res = await client.patch(
        f'{PREFIX}/menus/{menu_id}/submenus/{submenu_id}', json=update_data
    )
    print('Test request was sent to', res.url)
    assert res.status_code == 200
    updated_menu = schemas.SubmenuOut(**res.json())
    assert updated_menu.title == update_data['title']
    assert updated_menu.description == update_data['description']


async def test_update_submenu_not_exists(session, client, PREFIX, test_menus, test_submenus):
    menu_id = test_menus[0].id
    update_data = {
        'title': 'UPDATED test submenu title',
        'description': 'UPDATED test submenu description',
        'menu_id': '123456',
    }
    res = await client.patch(
        f'{PREFIX}/menus/{menu_id}/submenus/9876543210', json=update_data
    )
    assert res.status_code == 404
    assert res.json()['detail'] == 'submenu not found'


# Delete testing
async def test_delete_menu(session, client, PREFIX, test_menus, test_submenus):
    menu_id = test_menus[0].id
    result = (
        await session.execute(select(models.Submenu).filter(models.Submenu.menu_id == menu_id))
    )
    submenu_id = result.scalars().first().id

    res = await client.delete(f'{PREFIX}/menus/{menu_id}/submenus/{submenu_id}')
    print('Test request was sent to', res.url)
    assert res.status_code == 200
    assert res.json()['status'] is True
    assert res.json()['message'] == 'The submenu has been deleted'

    result = await session.execute(select(models.Submenu))
    all_submenus_list = result.scalars().all()
    assert len(all_submenus_list) == len(test_submenus) - 1


async def test_delete_menu_not_exists(session, client, PREFIX, test_menus):
    menu_id = test_menus[0].id
    res = await client.delete(f'{PREFIX}/menus/{menu_id}/submenus/9876543210')
    assert res.status_code == 404
    assert res.json()['detail'] == 'submenu not found'
