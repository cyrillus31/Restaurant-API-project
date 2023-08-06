from abc import ABC, abstractclassmethod
from typing import Union


from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status


from .. import models, schemas
from ..database import get_db
from .. import crud


class AbstractRepository(ABC):

    @abstractclassmethod
    def get(self): ...

    @abstractclassmethod
    def get_all(self): ...

    @abstractclassmethod
    def add(self): ...

    @abstractclassmethod
    def update(self): ...

    @abstractclassmethod
    def delete(self): ...


class NotificationRepository:
    @classmethod
    def delete_success(cls):
        return {"status": True, "message": "The menu has been deleted"}