from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.configurations.database import get_async_session
from src.models.sellers import Seller
from src.schemas import LoginSchema, Token

from src.utils import ACCESS_TOKEN_EXPIRE_MINUTES, verify_password, create_jwt_token

token_router = APIRouter(tags=["token"], prefix="/token")

# Больше не симулируем хранилище данных. Подключаемся к реальному, через сессию.
DBSession = Annotated[AsyncSession, Depends(get_async_session)]


# Ручка для получения JWT-токена по email и password
@token_router.post("/", status_code=status.HTTP_201_CREATED)
async def login_for_JWT_token(
    form_data: LoginSchema,
    session: DBSession,
):  # аутентификация пользователя по email и password
    # достаём из БД запись о пользователе по email
    # если такого пользователя не существует или пароль неверный, то
    # генерируем ошибку 401 - UNAUTHORIZED
    # иначе генерируем токен и возвращаем клиенту
    res = await session.execute(select(Seller).where(Seller.email == form_data.email))
    user = res.scalar_one_or_none()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    token = create_jwt_token(
        data={'sub': user.email}
    )
    return Token(
        access_token=token,
        token_type='Bearer',
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )