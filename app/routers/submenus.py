import logging

from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from .. import models, schemas, crud
from ..database import get_db


router = APIRouter(prefix="/api/v1/menus/{menu_id}/submenus", tags=["Submenus"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.MenuOut)
def create_submenu(menu_id, submenu: schemas.MenuCreate, db: Session = Depends(get_db)):
    db_menu = crud.get_submenu_by_title(db, title=submenu.title)

    if db_menu:
        raise HTTPException(
            status_code=400, detail="Submenu with this title already exists"
        )
    submenu = crud.create_submenu(menu_id=menu_id, db=db, submenu=submenu)

    return submenu


@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_menu(id, db: Session = Depends(get_db)):
    db_menu = crud.get_menu_by_id(db, id)
    if not db_menu:
        raise HTTPException(status_code=404, detail="menu not found")
    crud.delete_menu_by_id(db, id)
    return {"status": True, "message": "The menu has been deleted"}


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[schemas.MenuOut | None],
)
def read_submenus(
    menu_id,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    response_model=list[schemas.SubmenuOut],
):
    submenus = crud.get_submenus(menu_id, db, skip=skip, limit=limit)
    print("hi")
    return submenus


@router.get("/{id}", status_code=status.HTTP_200_OK)
def get_menu(id, db: Session = Depends(get_db)):
    db_submenu = crud.get_submenu_by_id(db, id=id)

    if not db_submenu:
        raise HTTPException(status_code=404, detail="menu not found")
    return db_submenu


@router.patch("/{id}", status_code=status.HTTP_200_OK)
def update_submenu(
    menu_id, id, submenu: schemas.MenuCreate, db: Session = Depends(get_db)
):
    db_submenu = crud.get_submenu_by_id(db, id)
    if not db_submenu:
        raise HTTPException(status_code=404, detail="menu not found")
    updated_submenu = crud.update_submenu_by_id(db=db, submenu=submenu, id=id)
    return updated_submenu
