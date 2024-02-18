from datetime import datetime, timedelta
import bcrypt


# В БД пароли в чистом виде не хранят, поэтому реализуем функцию для хэширования пароля
# Используем алгоритм bcrypt
def create_hashed_password(password: str):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password=password.encode('utf-8'), salt=salt).decode('utf-8')


# Верификатор пароля
def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password=password.encode('utf-8'), hashed_password=hashed_password)