from fastapi import APIRouter, BackgroundTasks, Depends, status

from .. import schemas
from ..services import MenuService

router = APIRouter(prefix='/api/v1/menus', tags=['Menus'])


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.MenuOut)
async def create_menu(background_tasks: BackgroundTasks, menu_data: schemas.MenuCreate, menu: MenuService = Depends(), ):
    return await menu.create(
        url_key='menus/',
        menu_data=menu_data,
        background_tasks=background_tasks,
    )


@router.delete('/{id}', status_code=status.HTTP_200_OK)
async def delete_menu(background_tasks: BackgroundTasks, id: str, menu: MenuService = Depends()):
    return await menu.delete(
        background_tasks=background_tasks,
        url_key=f'menus/{id}/',
        id=id
    )


@router.get('/', status_code=status.HTTP_200_OK, response_model=list[schemas.MenuOut | None])
async def read_menus(skip: int = 0, limit: int = 100, menu: MenuService = Depends()):
    return await menu.get_all(
        url_key='menus/',
        skip=skip,
        limit=limit
    )


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.MenuOut)
async def get_menu(id: str, menu: MenuService = Depends()):
    return await menu.get(
        url_key=f'menus/{id}/',
        id=id)


@router.patch('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.MenuOut)
async def update_menu(background_tasks: BackgroundTasks, menu_data: schemas.MenuCreate, id: str, menu: MenuService = Depends()):
    return await menu.update(
        background_tasks=background_tasks,
        menu_data=menu_data,
        id=id
    )
