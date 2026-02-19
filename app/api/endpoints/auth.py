from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.services.user import UserService
from app.schemas.user import UserCreate, UserResponse, UserLogin
from app.core.security import verify_password, create_user_access_token
from app.schemas.token import Token
from app.core.config import settings

router = APIRouter()


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    service = UserService(db)

    # Проверка на существующий email
    existing_user = await service.get_by_email(str(user_data.email))
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email уже зарегистрирован"
        )

    existing_user = await service.get_by_username(user_data.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким именем уже существует"
        )

    # Создание пользователя
    user = await service.create_user(user_data)

    return user


"""Если пользователь ввёл верные данные, то генерирует и отправляет JWT токен"""


@router.post("/login", response_model=Token, status_code=status.HTTP_200_OK)
async def login(user_data: UserLogin, db: AsyncSession = Depends(get_db)):
    service = UserService(db)
    user = await service.get_by_login(user_data.login)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Нет пользователя с таким email или username",
        )

    if verify_password(user_data.password, user.password_hash):
        time_delta = None
        if user_data.remember_me:
            time_delta = settings.REMEMBER_ME_ACCESS_TOKEN_EXPIRE
        token = create_user_access_token(user.id, time_delta)
        return Token(access_token=token, token_type="Bearer")

    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Неверный пароль")
