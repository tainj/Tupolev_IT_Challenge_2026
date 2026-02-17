from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# Движок (Engine)
engine = create_async_engine(settings.get_database_url, echo=settings.DEBUG)

# Фабрика сессий
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Базовый класс для моделей
Base = declarative_base()

async def get_db():
    async with async_session_maker() as session:
        yield session