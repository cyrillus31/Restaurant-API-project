from fastapi import APIRouter, Depends, status

from .. import schemas
from ..services import SubmenuService

router = APIRouter(
    prefix='/api/v1/menus/{menu_id}/submenus', tags=['Submenus'])


@router.post(
    '/', status_code=status.HTTP_201_CREATED, response_model=schemas.SubmenuOut
)
async def create_submenu(menu_id: str, submenu_data: schemas.SubmenuCreate, submenu: SubmenuService = Depends()):
    return await submenu.create(
        url_key=f'menus/{menu_id}/submenus/',
        menu_data=submenu_data,
        menu_id=menu_id
    )


@router.delete('/{id}', status_code=status.HTTP_200_OK)
async def delete_submenu(menu_id: str, id: str, submenu: SubmenuService = Depends()):
    return await submenu.delete(
        url_key=f'menus/{menu_id}/submenus/{id}/',
        id=id,
        menu_id=menu_id
    )


@router.get(
    '/',
    status_code=status.HTTP_200_OK,
    response_model=list[schemas.SubmenuOut],
)
async def read_submenus(menu_id: str, skip: int = 0, limit: int = 100, submenu: SubmenuService = Depends(),):
    return await submenu.get_all(
        url_key=f'menus/{menu_id}/submenus/',
        menu_id=menu_id,
        skip=skip,
        limit=limit
    )


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.SubmenuOut)
async def get_submenu(id: str, menu_id: str, submenu: SubmenuService = Depends()):
    return await submenu.get(
        url_key=f'menus/{menu_id}/submenus/{id}/',
        id=id,
        menu_id=menu_id
    )


@router.patch(
    '/{id}', status_code=status.HTTP_200_OK, response_model=schemas.SubmenuOut
)
async def update_submenu(
        menu_id: str, id: str, submenu_data: schemas.MenuCreate, submenu: SubmenuService = Depends()):
    return await submenu.update(submenu_data, id, menu_id=menu_id)
