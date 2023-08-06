from fastapi import APIRouter, Depends, status

from .. import schemas
from ..services import MenuService

router = APIRouter(prefix='/api/v1/menus', tags=['Menus'])


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.MenuOut)
async def create_menu(menu_data: schemas.MenuCreate, menu: MenuService = Depends()):
    return menu.create(menu_data)


@router.delete('/{id}', status_code=status.HTTP_200_OK)
def delete_menu(id, menu: MenuService = Depends()):
    return menu.delete(id)


@router.get('/', status_code=status.HTTP_200_OK, response_model=list[schemas.MenuOut | None])
def read_menus(skip: int = 0, limit: int = 100, menu: MenuService = Depends()):
    return menu.get_all(skip=skip, limit=limit)


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.MenuOut)
def get_menu(id, menu: MenuService = Depends()):
    return menu.get(id=id)


@router.patch('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.MenuOut)
def update_menu(menu_data: schemas.MenuCreate, id, menu: MenuService = Depends()):
    return menu.update(menu_data, id=id)
