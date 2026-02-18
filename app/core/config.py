from pydantic_settings import BaseSettings
from typing import Optional
from datetime import timedelta


class Settings(BaseSettings):
    # PostgreSQL
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "tupolev_db"
    POSTGRES_PORT: int = 5432

    # Строка подключения
    DATABASE_URL: Optional[str] = None

    # JWT и пароли
    SECRET_KEY: str = "your-super-secret-key-change-in-prod"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REMEMBER_ME_ACCESS_TOKEN_EXPIRE: timedelta = timedelta(days=30)

    # Приложение
    DEBUG: bool = True

    @property
    def get_access_token_expire_delta(self) -> timedelta:
        return timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)

    @property
    def get_database_url(self) -> str:
        if self.DATABASE_URL:
            return self.DATABASE_URL

        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@localhost:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


    @property
    def get_sync_database_url(self) -> str:
        """Для Alembic (sync, psycopg2)"""
        # Если задан DATABASE_URL, заменяем в нём драйвер на psycopg2
        if self.DATABASE_URL:
            return self.DATABASE_URL.replace("+asyncpg", "")
        # Иначе собираем строку с явным указанием psycopg2
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@localhost:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    class Config:
        env_file = ".env"
        extra = "ignore"
        case_sensitive = True


settings = Settings()