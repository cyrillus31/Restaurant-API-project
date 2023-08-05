from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from ..config import settings
# from ..repositories import MenuRepository
from ..services import MenuService
from .. import schemas, crud
from ..database import get_db

from starlette.requests import Request
from starlette.responses import Response
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from redis import asyncio as aioredis

router = APIRouter(prefix="/api/v1/menus", tags=["Menus"])


@router.on_event("startup")
async def startup():
    redis = aioredis.from_url(
        "redis://localhost", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


# @router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.MenuOut)
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_menu(menu_data: schemas.MenuCreate, menu: MenuService = Depends()):
    return menu.create(menu_data)


# @router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.MenuOut)
# def create_menu(menu: schemas.MenuCreate, db: Session = Depends(get_db)):
    # db_menu = crud.get_menu_by_title(db, title=menu.title)

    # if db_menu:
    # raise HTTPException(
    # status_code=400, detail="Menu with this title already exists"
    # )
    # menu = crud.create_menu(db, menu)

    # return menu


@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_menu(id, menu: MenuService = Depends()):
    return menu.delete(id)

# @router.delete("/{id}", status_code=status.HTTP_200_OK)
# def delete_menu(id, db: Session = Depends(get_db)):
    # db_menu = crud.get_menu_by_id(db, id)
    # if not db_menu:
    # raise HTTPException(status_code=404, detail="menu not found")
    # crud.delete_menu_by_id(db, id)
    # return {"status": True, "message": "The menu has been deleted"}


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[schemas.MenuOut])
def read_menus(skip: int = 0, limit: int = 100, menu: MenuService = Depends()):
    return menu.get_all(skip=skip, limit=limit)

# @router.get("/", status_code=status.HTTP_200_OK, response_model=list[schemas.MenuOut])
# def read_menus(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # menus = crud.get_menus(db, skip=skip, limit=limit)
    # for db_menu in menus:
    # db_menu.submenus_count = crud.get_menu_submenus_count(db, db_menu.id)
    # db_menu.dishes_count = crud.get_menus_dishes_count(db, db_menu.id)

    # return menus


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.MenuOut)
def get_menu(id, menu: MenuService = Depends()):
    return menu.get(id=id)


# @router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.MenuOut)
# def get_menu(id, db: Session = Depends(get_db)):
    # db_menu = crud.get_menu_by_id(db, id=id)

    # if not db_menu:
    # raise HTTPException(status_code=404, detail="menu not found")
    # db_menu.submenus_count = crud.get_menu_submenus_count(db, id)
    # db_menu.dishes_count = crud.get_menus_dishes_count(db, id)
    # return db_menu

@router.patch("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.MenuOut)
def update_menu(menu_data: schemas.MenuCreate, id, menu: MenuService = Depends()):
    return menu.update(menu_data, id=id)


# @router.patch("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.MenuOut)
# def update_menu(id, menu: schemas.MenuCreate, db: Session = Depends(get_db)):
    # db_menu = crud.get_menu_by_id(db, id)
    # if not db_menu:
    # raise HTTPException(status_code=404, detail="menu not found")
    # updated_menu = crud.update_menu_by_id(db=db, menu=menu, id=id)
    # return updated_menu
