from fastapi import APIRouter, Depends, status

from .. import schemas
from ..services import DishService

router = APIRouter(
    prefix='/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes', tags=['Dishes']
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.DishOut)
def create_dish(submenu_id, dish_data: schemas.DishCreate, dish: DishService = Depends()):
    return dish.create(dish_data, submenu_id=submenu_id)


@router.delete('/{id}', status_code=status.HTTP_200_OK)
def delete_dish(submenu_id, id, dish: DishService = Depends()):
    return dish.delete(id, submenu_id=submenu_id)


@router.get(
    '/',
    status_code=status.HTTP_200_OK,
    response_model=list[schemas.DishOut | None],
)
def read_dishes(
    submenu_id,
    skip: int = 0,
    limit: int = 100,
    dish: DishService = Depends(),
):
    return dish.get_all(submenu_id=submenu_id, skip=skip, limit=limit)


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.DishOut)
def get_dish(id, submenu_id, dish: DishService = Depends()):
    return dish.get(id=id, submenu_id=submenu_id)


@router.patch('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.DishOut)
def update_dish(
    submenu_id, id, dish_data: schemas.DishCreate, dish: DishService = Depends()
):
    return dish.update(dish_data, id=id, submenu_id=submenu_id)
