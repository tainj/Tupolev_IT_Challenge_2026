from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash
from app.models import User
from app.schemas.user import UserCreate, UserUpdate
from jose import jwt
from app.core.config import settings


class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, user_id: int) -> User | None:
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> User | None:
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def get_by_username(self, username: str) -> User | None:
        result = await self.db.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()

    async def get_by_login(self, login: str) -> User | None:
        result = await self.db.execute(select(User).where(or_(User.email == login, User.username == login)))
        return result.scalar_one_or_none()

    async def create_user(self, userdata: UserCreate) -> User:
        user = User(
            email=userdata.email,
            username=userdata.username,
            password_hash=get_password_hash(userdata.password)
        )
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def update_user(self, user: User, update_data: UserUpdate) -> User:
        for field, value in update_data.model_dump(exclude_unset=True).items():
            if field == "password":
                value = get_password_hash(value)
            setattr(user, field, value)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def delete_user(self, user: User) -> None:
        await self.db.delete(user)
        await self.db.commit()

    async def get_user_from_jwt(self, token: str) -> User | None:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
            user_id = payload.get("sub")
            print(user_id)
            if user_id is None:
                return None
        except:
            return None
        user = await self.get_by_id(int(user_id))
        return user

