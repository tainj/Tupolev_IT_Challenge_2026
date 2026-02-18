from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt, JWTError
from passlib.context import CryptContext
from app.core.config import settings
from app.models import User

# Контекст для хеширования паролей (bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверка пароля: ввод пользователя == хеш в базе"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Создание хеша из пароля (перед записью в БД)"""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Создание JWT токена для пользователя"""
    to_encode = data.copy()

    # Время жизни токена (из конфига или по умолчанию)
    expire = datetime.now(timezone.utc) + (expires_delta or settings.get_access_token_expire_delta)

    to_encode.update({"exp": expire})

    # Подпись токена (ключ из конфига)
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

'''Создаёт токен с id пользователя'''
def create_user_access_token(id: str, expires_delta: Optional[timedelta] = None) -> str:
    return create_access_token({"sub": str(id)}, expires_delta)