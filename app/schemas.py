from pydantic import BaseModel


class MenuCreate(BaseModel):
    title: str
    description: str | None


class SubmenuCreate(BaseModel):
    title: str
    description: str | None


class MenuOut(BaseModel):
    id: str
    title: str
    description: str | None
    submenus_count: int
    dishes_count: int

    class Config:
        from_attributes = True


class SubmenuOut(BaseModel):
    id: str
    title: str
    description: str | None
    dishes_count: int

    class Config:
        from_attributes = True


class DishCreate(BaseModel):
    title: str
    description: str | None
    price: str


class DishOut(BaseModel):
    id: str
    title: str
    description: str | None
    price: str

    class Config:
        from_attributes = True
