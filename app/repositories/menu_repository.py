from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .. import crud, models, schemas
from ..database import get_session


class MenuRepository:

    def __init__(self, db: AsyncSession = Depends(get_session)) -> None:
        self.db = db
        self.orm_model = models.Menu
        self.detail_404 = 'menu not found'
        self.detail_400 = 'Menu with this title already exists'

    async def get_all(self, skip: int = 0, limit: int = 100, **kwargs) -> list[models.Menu | models.Submenu | models.Dish | None]:
        # menus = self.db.query(self.orm_model).filter_by(**kwargs).offset(
            # skip).limit(limit).all()
        lookup_query = select(self.orm_model).filter_by(**kwargs).offset(skip).limit(limit)
        result = await self.db.execute(lookup_query)
        menus = result.scalars().all()

        # count submenus and dishes
        for db_menu in menus:
            db_menu.submenus_count = await crud.get_menu_submenus_count(
                self.db, db_menu.id)
            db_menu.dishes_count = await crud.get_menus_dishes_count(
                self.db, db_menu.id)
        return menus

    async def get(self, **kwargs):
        menu = self.db.query(
            self.orm_model).filter_by(**kwargs).first()
        if not menu:
            raise HTTPException(
                status_code=404, detail=f'{self.detail_404}')

        # count submenus and dishes
        menu.submenus_count = await crud.get_menu_submenus_count(self.db, menu.id)
        menu.dishes_count = await crud.get_menus_dishes_count(self.db, menu.id)
        return menu

    async def add(self, menu: schemas.MenuCreate | schemas.SubmenuCreate | schemas.DishCreate, **kwargs) -> models.Menu | models.Submenu | models.Dish | None:
        # menu_exists = self.db.query(self.orm_model).filter(
            # self.orm_model.title == menu.title).filter_by(**kwargs).first()
        lookup_query = select(self.orm_model).filter(self.orm_model.title == menu.title).filter_by(**kwargs)
        result = await self.db.execute(lookup_query)
        menu_exists = result.scalars().first()
        if menu_exists:
            raise HTTPException(
                status_code=400, detail=f'{self.detail_400}'
            )
        new_menu = self.orm_model(**menu.dict(), **kwargs)
        self.db.add(new_menu)
        await self.db.commit()
        await self.db.refresh(new_menu)
        return new_menu

    def delete(self, id: str, **kwargs) -> None:
        menu_exists = self.get(id=id, **kwargs)
        if not menu_exists:
            raise HTTPException(
                status_code=404, detail=f'{self.detail_404}')
        self.db.query(self.orm_model).filter(
            self.orm_model.id == id).delete()
        self.db.commit()

    def update(self, menu: schemas.MenuCreate | schemas.SubmenuCreate | schemas.DishCreate, id: str, **kwargs) -> models.Menu | models.Submenu | models.Dish | None:
        # menu_exists = self.get(id=id)
        menu_exists = self.db.query(self.orm_model).filter(
            self.orm_model.id == id).filter_by(**kwargs).first()
        if not menu_exists:
            raise HTTPException(
                status_code=404, detail=f'{self.detail_404}')

        update_menu = self.db.query(
            self.orm_model).filter(self.orm_model.id == id)
        update_menu.update(menu.dict(), synchronize_session=False)
        self.db.commit()
        return update_menu.first()
