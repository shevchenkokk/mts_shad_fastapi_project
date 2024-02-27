from pydantic import BaseModel

__all__ = ["Token"]


# Класс для представления JWT-токена
class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: int