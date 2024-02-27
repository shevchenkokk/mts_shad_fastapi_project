import os
from datetime import datetime, timedelta
import bcrypt
from jose import jwt, JWTError

from typing import Optional

from fastapi import status, HTTPException, Header
from fastapi.security import OAuth2PasswordBearer


ACCESS_TOKEN_EXPIRE_MINUTES = 5
ALGORITHM = "HS256"
# Должно оставаться секретным
JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']

# Механизм для проверки токена из заголовков запроса
reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="api/v1/token",
    scheme_name="JWT"
)


# В БД пароли в чистом виде не хранят, поэтому реализуем функцию для хэширования пароля
# Используем алгоритм bcrypt
def create_hashed_password(password: str):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password=password.encode('utf-8'), salt=salt).decode('utf-8')


# Верификатор пароля
def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password=password.encode('utf-8'), hashed_password=hashed_password.encode('utf-8'))


# Создание JWT-токена
def create_jwt_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'authorized': True, 'exp': expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Проверка токена
def verify_token(authorization: Optional[str] = Header(None)):
    try:
        if authorization:
            token_type, _, token = authorization.partition(' ')
            if token_type == 'Bearer' and token:
                payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
                email = payload.get('sub')
                if email is None:
                    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
                return payload
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED
    )