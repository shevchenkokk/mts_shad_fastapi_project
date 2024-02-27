from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .books import Book

from .base import BaseModel


class Seller(BaseModel):
    __tablename__ = "sellers_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    password: Mapped[int] =  mapped_column(String(100), nullable=False)

    books: Mapped[list['Book']] = relationship('Book', cascade='all, delete-orphan')
