from typing import Optional

from pydantic import BaseModel  # EmailStr
from datetime import datetime

# from sqlalchemy.dialects.postgresql import UUID


class MenuCreate(BaseModel):
    title: str
    description: Optional[str]


class SubmenuCreate(BaseModel):
    title: str
    description: Optional[str]


class MenuOut(BaseModel):
    id: str
    title: str
    description: Optional[str] | None
    # submenus_count: list
    # dishes_count: int

    class Config:
        from_attributes = True


class SubmenuOut(BaseModel):
    id: str
    title: str
    description: Optional[str] | None
    # submenus_count: list
    # dishes_count: list

    class Config:
        from_attributes = True


class DishCreate(BaseModel):
    title: str
    description: Optional[str]
    price: float


class DishOut(BaseModel):
    title: str
    description: Optional[str]
    price: float

    class Config:
        from_attributes = True
