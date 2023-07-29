import uuid

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text  # to insert sql functions as a text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from .database import Base


class Menu(Base):
    __tablename__ = "menu"

    id = Column(
        String, primary_key=True, nullable=False, default=lambda: str(uuid.uuid4())
    )
    title = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )

    submenus = relationship("Submenu")
    submenus_count = 0
    dishes_count = 0


class Submenu(Base):
    __tablename__ = "submenu"

    id = Column(
        String, primary_key=True, nullable=False, default=lambda: str(uuid.uuid4())
    )
    title = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    menu_id = Column(String, ForeignKey("menu.id", ondelete="CASCADE"), nullable=False)

    dishes_relation = relationship("Dish")
    dishes_count = 0


class Dish(Base):
    __tablename__ = "dish"
    id = Column(
        String, primary_key=True, nullable=False, default=lambda: str(uuid.uuid4())
    )
    title = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)
    price = Column(String, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    submenu_id = Column(
        String, ForeignKey("submenu.id", ondelete="CASCADE"), nullable=False
    )
