from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from .. import schemas, crud
from ..database import get_db


router = APIRouter(prefix="/api/v1/menus/{menu_id}/submenus", tags=["Submenus"])


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.SubmenuOut
)
def create_submenu(menu_id, submenu: schemas.MenuCreate, db: Session = Depends(get_db)):
    db_menu = crud.get_submenu_by_title(db, title=submenu.title)

    if db_menu:
        raise HTTPException(
            status_code=400, detail="Submenu with this title already exists"
        )
    submenu = crud.create_submenu(menu_id=menu_id, db=db, submenu=submenu)

    return submenu


@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_submenu(menu_id, id, db: Session = Depends(get_db)):
    db_submenu = crud.get_submenu_by_id(db, id)

    if not db_submenu:
        raise HTTPException(status_code=404, detail="submenu not found")

    crud.delete_submenu_by_id(db, id)

    return {"status": True, "message": "The menu has been deleted"}


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[schemas.SubmenuOut],
)
def read_submenus(
    menu_id,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    # response_model=list[schemas.SubmenuOut],
):
    submenus = crud.get_submenus(menu_id, db, skip=skip, limit=limit)
    for db_submenu in submenus:
        db_submenu.dishes_count = crud.get_sumbenus_dishes_count(db, menu_id)

    return submenus


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.SubmenuOut)
def get_menu(id, db: Session = Depends(get_db)):
    db_submenu = crud.get_submenu_by_id(db, id=id)

    if not db_submenu:
        raise HTTPException(status_code=404, detail="submenu not found")
    db_submenu.dishes_count = crud.get_sumbenus_dishes_count(db, id)
    return db_submenu


@router.patch(
    "/{id}", status_code=status.HTTP_200_OK, response_model=schemas.SubmenuOut
)
def update_submenu(
    menu_id, id, submenu: schemas.MenuCreate, db: Session = Depends(get_db)
):
    db_submenu = crud.get_submenu_by_id(db, id)

    if not db_submenu:
        raise HTTPException(status_code=404, detail="menu not found")

    updated_submenu = crud.update_submenu_by_id(db=db, submenu=submenu, id=id)
    return updated_submenu
