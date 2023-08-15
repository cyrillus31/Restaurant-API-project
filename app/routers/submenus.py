from fastapi import APIRouter, BackgroundTasks, Depends, status

from .. import schemas
from ..services import SubmenuService

router = APIRouter(
    prefix='/api/v1/menus/{menu_id}/submenus', tags=['Submenus'])


@router.post(
    '/', status_code=status.HTTP_201_CREATED, response_model=schemas.SubmenuOut
)
async def create_submenu(background_tasks: BackgroundTasks, menu_id: str, submenu_data: schemas.SubmenuCreate, submenu: SubmenuService = Depends(), id: str | None = None):
    return await submenu.create(
        url_key=f'menus/{menu_id}/submenus/',
        menu_data=submenu_data,
        background_tasks=background_tasks,
        menu_id=menu_id
    )


@router.delete('/{id}', status_code=status.HTTP_200_OK)
async def delete_submenu(background_tasks: BackgroundTasks, menu_id: str, id: str, submenu: SubmenuService = Depends()):
    return await submenu.delete(
        background_tasks=background_tasks,
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
        background_tasks: BackgroundTasks, menu_id: str, id: str, submenu_data: schemas.MenuCreate, submenu: SubmenuService = Depends()):
    return await submenu.update(background_tasks=background_tasks, menu_data=submenu_data, id=id, menu_id=menu_id)
