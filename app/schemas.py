from typing import Optional

from pydantic import BaseModel


class MenuCreate(BaseModel):
    title: str
    description: Optional[str]


class SubmenuCreate(BaseModel):
    title: str
    description: Optional[str]


class MenuOut(BaseModel):
    id: str
    title: str
    description: Optional[str]
    submenus_count: int
    dishes_count: int

    class Config:
        from_attributes = True


class SubmenuOut(BaseModel):
    id: str
    title: str
    description: Optional[str]
    dishes_count: int

    class Config:
        from_attributes = True


class DishCreate(BaseModel):
    title: str
    description: Optional[str]
    price: str


class DishOut(BaseModel):
    id: str
    title: str
    description: Optional[str]
    price: str

    class Config:
        from_attributes = True
