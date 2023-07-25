import logging

from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from .. import schemas, crud
from ..database import get_db


router = APIRouter(
    prefix="/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes", tags=["Dishes"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.DishOut)
def create_dish(submenu_id, dish: schemas.DishCreate, db: Session = Depends(get_db)):
    db_dish = crud.get_dish_by_title(db, title=dish.title)

    if db_dish:
        raise HTTPException(
            status_code=400, detail="Dish with this title already exists"
        )
    dish = crud.create_dish(submenu_id=submenu_id, db=db, dish=dish)

    return dish


@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_dish(submenu_id, id, db: Session = Depends(get_db)):
    db_dish = crud.get_dish_by_id(db, id)

    if not db_dish:
        raise HTTPException(status_code=404, detail="dish not found")

    crud.delete_dish_by_id(db, id)

    return {"status": True, "message": "The menu has been deleted"}


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[schemas.MenuOut | None],
)
def read_dishes(
    submenu_id,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    response_model=list[schemas.DishOut],
):
    submenus = crud.get_dishes(submenu_id, db, skip=skip, limit=limit)

    print("hi")
    return submenus


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.DishOut)
def get_dish(id, db: Session = Depends(get_db)):
    db_dish = crud.get_dish_by_id(db, id=id)

    if not db_dish:
        raise HTTPException(status_code=404, detail="dish not found")
    return db_dish


@router.patch("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.DishOut)
def update_dish(
    submenu_id, id, dish: schemas.DishCreate, db: Session = Depends(get_db)
):
    db_dish = crud.get_dish_by_id(db, id)

    if not db_dish:
        raise HTTPException(status_code=404, detail="dish not found")

    updated_dish = crud.update_dish_by_id(db=db, dish=dish, id=id)
    return updated_dish
