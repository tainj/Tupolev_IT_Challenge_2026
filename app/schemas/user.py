from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime
from typing import Optional


# === ЗАПРОСЫ (Request) ===


class UserCreate(BaseModel):
    """Схема для регистрации пользователя"""

    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50, pattern="^[a-zA-Z0-9_]+$")
    password: str = Field(..., min_length=8, description="Минимум 8 символов")


class UserLogin(BaseModel):
    """Схема для входа"""

    login: str
    password: str
    remember_me: bool


class UserUpdate(BaseModel):
    """Схема для обновления профиля"""

    email: Optional[EmailStr] = None
    username: Optional[str] = Field(
        None, min_length=3, max_length=50, pattern="^[a-zA-Z0-9_]+$"
    )
    password: Optional[str] = Field(
        None, min_length=8, description="Минимум 8 символов"
    )
    is_active: Optional[bool] = None


# === ОТВЕТЫ (Response) ===


class UserResponse(BaseModel):
    """Схема ответа с данными пользователя"""

    id: int
    email: str
    username: str
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)  # Для работы с SQLAlchemy моделями


class UserListResponse(BaseModel):
    """Схема для списка пользователей"""

    users: list[UserResponse]
    total: int
