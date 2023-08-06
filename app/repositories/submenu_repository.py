from abc import ABC, abstractclassmethod
from typing import Union

from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status

from .. import models, schemas
from ..database import get_db
from .. import crud
from .menu_repository import MenuRepository


class SubmenuRepository(MenuRepository):
    orm_model = models.Submenu
    schema = schemas.SubmenuCreate
    detail_404 = "submenu not found"
    detail_400 = "Submenu with this title already exists"
