from fastapi import Request, Response
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.schemas.auth_schema import ApiResponse, UserLoginRequest, UserRegisterRequest
from app.services.auth_service import AuthService
from app.utils.cookies import clear_auth_cookies, set_auth_cookies


async def register_controller(payload: UserRegisterRequest, db: AsyncIOMotorDatabase):
    # Handle user registration
    auth_service = AuthService(db)
    user = await auth_service.register_user(payload.full_name, payload.email, payload.password)
    return ApiResponse(message="User registered successfully", data={"user": user})


async def login_controller(payload: UserLoginRequest, response: Response, db: AsyncIOMotorDatabase):
    # Handle login and set cookies
    auth_service = AuthService(db)
    user, access_token, refresh_token = await auth_service.login_user(payload.email, payload.password)
    set_auth_cookies(response, access_token, refresh_token)
    return ApiResponse(message="Login successful", data={"user": user})


async def refresh_token_controller(request: Request, response: Response, db: AsyncIOMotorDatabase):
    # Rotate refresh token and update cookies
    refresh_token = request.cookies.get("refresh_token")
    auth_service = AuthService(db)
    user, new_access, new_refresh = await auth_service.refresh_session(refresh_token)
    set_auth_cookies(response, new_access, new_refresh)
    return ApiResponse(message="Tokens refreshed successfully", data={"user": user})


async def logout_controller(request: Request, response: Response, db: AsyncIOMotorDatabase):
    # Revoke session and clear cookies
    refresh_token = request.cookies.get("refresh_token")
    auth_service = AuthService(db)
    await auth_service.logout_user(refresh_token)
    clear_auth_cookies(response)
    return ApiResponse(message="Logout successful")


async def get_me_controller(current_user: dict):
    # Return logged-in user profile
    return ApiResponse(message="Profile retrieved successfully", data={"user": current_user})
