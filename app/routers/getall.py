from fastapi import APIRouter, Depends, status

from ..services import GetAllService

router = APIRouter(prefix='/api/v1/getall', tags=['Get all Menus, Submenus and Dishes'])


@router.get('/', status_code=status.HTTP_200_OK,)
async def get_all(getall: GetAllService = Depends(),) -> dict:
    return await getall.get_all(
        url_key='getall/',
    )
