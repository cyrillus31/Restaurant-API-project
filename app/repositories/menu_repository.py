from fastapi import Depends, HTTPException
from sqlalchemy import delete, select, update
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
        # menu = self.db.query(
        # self.orm_model).filter_by(**kwargs).first()
        lookup_query = select(self.orm_model).filter_by(**kwargs)
        result = await self.db.execute(lookup_query)
        menu = result.scalars().first()
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

    async def delete(self, id: str, **kwargs) -> None:
        lookup_query = select(self.orm_model).filter_by(id=id)
        result = await self.db.execute(lookup_query)
        menu_exists = result.scalars().first()
        if not menu_exists:
            raise HTTPException(
                status_code=404, detail=f'{self.detail_404}')
        # self.db.query(self.orm_model).filter(
            # self.orm_model.id == id).delete()
        # self.db.commit()
        delete_query = delete(self.orm_model).filter_by(id=id)
        result = await self.db.execute(delete_query)
        await self.db.commit()

    async def update(self, menu: schemas.MenuCreate | schemas.SubmenuCreate | schemas.DishCreate, id: str, **kwargs) -> models.Menu | models.Submenu | models.Dish | None:
        # menu_exists = self.db.query(self.orm_model).filter(
        # self.orm_model.id == id).filter_by(**kwargs).first()
        lookup_query = select(self.orm_model).filter_by(id=id)
        result = await self.db.execute(lookup_query)
        menu_exists = result.scalars().first()
        if not menu_exists:
            raise HTTPException(
                status_code=404, detail=f'{self.detail_404}')

        update_query = update(self.orm_model).where(self.orm_model.id == id).values({**menu.dict(), **kwargs})
        result = await self.db.execute(update_query)
        # update_menu = await self.db.query(
        # self.orm_model).filter(self.orm_model.id == id)

        await self.db.commit()
        result = await self.db.execute(lookup_query)
        updated_menu = result.scalars().first()
        return updated_menu
