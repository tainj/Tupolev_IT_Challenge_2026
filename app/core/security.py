from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt
from passlib.context import CryptContext
from app.core.config import settings

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
    expire = datetime.now(timezone.utc) + (
        expires_delta or settings.get_access_token_expire_delta
    )

    to_encode.update({"exp": expire})

    # Подпись токена (ключ из конфига)
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


"""Создаёт токен с id пользователя"""


def create_user_access_token(id: str, expires_delta: Optional[timedelta] = None, claims: Optional[list[str]] = []) -> str:
    claims_string = ""
    for i in range(len(claims)):
        claims_string += claims[i]
        if i != len(claims) - 1:
            claims_string += ","
    return create_access_token({"sub": str(id), "claims":claims_string}, expires_delta)

def has_claims(token: str, check_claims: list[str]) -> bool:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=settings.ALGORITHM
        )
        claims = payload.get("claims").split()
        if not claims:
            return False
        for c in check_claims:
            if c not in claims:
                return False
        return True
    except Exception():
        return False