from fastapi import APIRouter, Depends, Request, Response, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.controllers.auth_controller import (
    get_me_controller,
    login_controller,
    logout_controller,
    refresh_token_controller,
    register_controller,
)
from app.database import get_database
from app.limiter import limiter
from app.middleware.auth_middleware import get_current_user
from app.schemas.auth_schema import UserLoginRequest, UserRegisterRequest

router = APIRouter(prefix="/api/auth", tags=["Auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
async def register(request: Request, payload: UserRegisterRequest, db: AsyncIOMotorDatabase = Depends(get_database)):
    # Register new user
    return await register_controller(payload, db)


@router.post("/login", status_code=status.HTTP_200_OK)
@limiter.limit("5/minute")
async def login(request: Request, payload: UserLoginRequest, response: Response, db: AsyncIOMotorDatabase = Depends(get_database)):
    # Login user and return cookies
    return await login_controller(payload, response, db)


@router.post("/refresh-token", status_code=status.HTTP_200_OK)
@limiter.limit("10/minute")
async def refresh_token(request: Request, response: Response, db: AsyncIOMotorDatabase = Depends(get_database)):
    # Rotate refresh token
    return await refresh_token_controller(request, response, db)


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(request: Request, response: Response, db: AsyncIOMotorDatabase = Depends(get_database)):
    # Logout and clear cookies
    return await logout_controller(request, response, db)


@router.get("/me", status_code=status.HTTP_200_OK)
async def get_me(current_user: dict = Depends(get_current_user)):
    # Get current user profile
    return await get_me_controller(current_user)
