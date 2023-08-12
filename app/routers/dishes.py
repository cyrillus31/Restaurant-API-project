from fastapi import APIRouter, Depends, status

from .. import schemas
from ..services import DishService

router = APIRouter(
    prefix='/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes', tags=['Dishes']
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.DishOut)
async def create_dish(menu_id: str, submenu_id: str, dish_data: schemas.DishCreate, dish: DishService = Depends()):
    return await dish.create(
        url_key=f'menus/{menu_id}/submenus/{submenu_id}/dishes/',
        menu_data=dish_data,
        submenu_id=submenu_id
    )


@router.delete('/{id}', status_code=status.HTTP_200_OK)
async def delete_dish(menu_id: str, submenu_id: str, id: str, dish: DishService = Depends()):
    return await dish.delete(
        url_key=f'menus/{menu_id}/submenus/{submenu_id}/dishes/{id}/',
        id=id,
        submenu_id=submenu_id
    )


@router.get(
    '/',
    status_code=status.HTTP_200_OK,
    response_model=list[schemas.DishOut | None],
)
async def read_dishes(
    menu_id: str,
    submenu_id: str,
    skip: int = 0,
    limit: int = 100,
    dish: DishService = Depends(),
):
    return await dish.get_all(
        url_key=f'menus/{menu_id}/submenus/{submenu_id}/dishes/',
        submenu_id=submenu_id,
        skip=skip,
        limit=limit
    )


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.DishOut)
async def get_dish(id: str, submenu_id: str, menu_id: str, dish: DishService = Depends()):
    return await dish.get(
        url_key=f'menus/{menu_id}/submenus/{submenu_id}/dishes/{id}/',
        id=id,
        submenu_id=submenu_id)


@router.patch('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.DishOut)
async def update_dish(
    submenu_id: str,
    id: str,
    dish_data: schemas.DishCreate, dish: DishService = Depends()
):
    return await dish.update(dish_data, id=id, submenu_id=submenu_id)
