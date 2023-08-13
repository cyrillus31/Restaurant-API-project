from sqlalchemy import select

from app import models, schemas

# pytestmark = pytest.mark.anyio
# CRUD testing


# Create testing
async def test_create_menu(session, client, PREFIX):
    create_data = {
        'title': 'test menu 1111 title',
        'description': 'test menu 1 description',
    }
    res = await client.post(f'{PREFIX}/menus/', json=create_data)
    print('Test request was sent to', res.url)
    assert res.status_code == 201
    created_menu = schemas.MenuOut(**res.json())
    assert created_menu.title == create_data['title']
    assert created_menu.description == create_data['description']


# Read testing
async def test_get_menu(session, client, PREFIX, test_menus):
    test_menu_id = test_menus[0].id
    res = await client.get(f'{PREFIX}/menus/{test_menu_id}')
    assert res.status_code == 200
    response_menu = schemas.MenuOut(**res.json())
    assert response_menu.title == test_menus[0].title


async def test_get_menu_not_exists(session, client, PREFIX, test_menus):
    res = await client.get(f'{PREFIX}/menus/9876543210')
    assert res.status_code == 404
    assert res.json()['detail'] == 'menu not found'


# Read multiple testing

async def test_read_menus(session, client, PREFIX, test_menus):
    res = await client.get(f'{PREFIX}/menus/')
    response_data = res.json()
    validated_menus_list = [schemas.MenuOut(**menu) for menu in response_data]

    assert res.status_code == 200
    assert len(validated_menus_list) == len(test_menus)


async def test_read_menus_empty(session, client, PREFIX):
    res = await client.get(f'{PREFIX}/menus/')
    assert res.status_code == 200
    assert res.json() == []


# Update testing

async def test_update_menu(session, client, PREFIX, test_menus):
    test_menu_id = test_menus[0].id
    update_data = {
        'title': 'UPDATED test menu 1 title',
        'description': 'UPDATED test menu 1 description',
    }
    res = await client.patch(f'{PREFIX}/menus/{test_menu_id}', json=update_data)
    print('Test request was sent to', res.url)
    assert res.status_code == 200
    updated_menu = schemas.MenuOut(**res.json())
    assert updated_menu.title == update_data['title']
    assert updated_menu.description == update_data['description']


async def test_update_menu_not_exists(session, client, PREFIX, test_menus):
    update_data = {
        'title': 'UPDATED test menu 1 title',
        'description': 'UPDATED test menu 1 description',
    }
    res = await client.patch(f'{PREFIX}/menus/9876543210', json=update_data)
    assert res.status_code == 404
    assert res.json()['detail'] == 'menu not found'


# Delete testing

async def test_delete_menu(session, client, PREFIX, test_menus):
    test_menu_id = test_menus[0].id
    res = await client.delete(f'{PREFIX}/menus/{test_menu_id}')
    print('Test request was sent to', res.url)
    assert res.status_code == 200
    assert res.json()['status'] is True
    assert res.json()['message'] == 'The menu has been deleted'

    # all_menus_list = session.get(models.Menu).all()
    result = await session.execute(select(models.Menu))
    all_menus_list = result.scalars().all()
    assert len(all_menus_list) == len(test_menus) - 1


async def test_delete_menu_not_exists(session, client, PREFIX, test_menus):
    res = await client.delete(f'{PREFIX}/menus/9876543210')
    assert res.status_code == 404
    assert res.json()['detail'] == 'menu not found'
