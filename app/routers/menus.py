import logging

from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter

from sqlalchemy.orm import Session

from sqlalchemy.exc import IntegrityError

from .. import models, schemas, crud

from ..database import get_db


router = APIRouter(prefix="/api/v1/menus", tags=["Menus"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.MenuOut)
def create_menu(menu: schemas.MenuCreate, db: Session = Depends(get_db)):
    db_menu = crud.get_menu_by_title(db, title=menu.title)

    if db_menu:
        raise HTTPException(
            status_code=400, detail="Menu with this title already exists"
        )
    menu = crud.create_menu(db, menu)

    print("hello")
    print(menu.submenus_count)
    return menu


@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_menu(id, db: Session = Depends(get_db)):
    db_menu = crud.get_menu_by_id(db, id)
    if not db_menu:
        raise HTTPException(status_code=404, detail="menu not found")
    crud.delete_menu_by_id(db, id)
    return {"status": True, "message": "The menu has been deleted"}


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[schemas.MenuOut])
def read_menus(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    menus = crud.get_menus(db, skip=skip, limit=limit)
    return menus


@router.get("/{id}", status_code=status.HTTP_200_OK)
def get_menu(id, db: Session = Depends(get_db)):
    db_menu = crud.get_menu_by_id(db, id=id)

    if not db_menu:
        raise HTTPException(status_code=404, detail="menu not found")
    return db_menu


@router.patch("/{id}", status_code=status.HTTP_200_OK)
def update_menu(id, menu: schemas.MenuCreate, db: Session = Depends(get_db)):
    db_menu = crud.get_menu_by_id(db, id)
    if not db_menu:
        raise HTTPException(status_code=404, detail="menu not found")
    updated_menu = crud.update_menu_by_id(db=db, menu=menu, id=id)
    return updated_menu
