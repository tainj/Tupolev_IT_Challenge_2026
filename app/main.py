from fastapi import FastAPI, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import auth
from typing import Annotated
from app.services.user import UserService
from app.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import has_claims

app = FastAPI(
    title="TupolevITChallenge2026",
    version="1.0.0",
    description="API для проекта",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Роуты
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])


@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.get("/")
async def root(
    authorization: Annotated[str | None, Header(alias="Authorization")] = None,
    db: AsyncSession = Depends(get_db),
):
    if authorization:
        user_service = UserService(db)
        user = None
        token = ""
        if len(authorization.split(" ")) == 2:
            token = authorization.split(" ")[1]
            user = await user_service.get_user_from_jwt(token)
        if user:
            return {
                "message": f"Welcome to TupolevITChallenge2026 API, {user.username}. Has user claim: {has_claims(token, ["user"])}. Has admin claim: {has_claims(token, ["admin"])}"
            }
    return {"message": "Welcome to TupolevITChallenge2026 API"}
