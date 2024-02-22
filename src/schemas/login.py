from pydantic import BaseModel

__all__ = ["LoginSchema"]


# Класс для представления структуры входящего запроса при получении токена
class LoginSchema(BaseModel):
    email: str
    password: str