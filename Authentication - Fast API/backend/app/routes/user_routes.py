from fastapi import APIRouter, Depends, Query, Response, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.controllers.user_controller import (
    admin_delete_user_controller,
    admin_get_user_controller,
    admin_list_users_controller,
    admin_update_user_controller,
    delete_my_account_controller,
    get_my_profile_controller,
    update_my_profile_controller,
)
from app.database import get_database
from app.middleware.auth_middleware import get_admin_user, get_current_user
from app.schemas.user_schema import AdminUserUpdateRequest, UserUpdateRequest

router = APIRouter(prefix="/api/users", tags=["Users"])


@router.get("/me", status_code=status.HTTP_200_OK)
async def get_my_profile(current_user: dict = Depends(get_current_user)):
    # Get current user profile
    return await get_my_profile_controller(current_user)


@router.patch("/me", status_code=status.HTTP_200_OK)
async def update_my_profile(
    payload: UserUpdateRequest,
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database),
):
    # Update current user profile
    return await update_my_profile_controller(payload, current_user, db)


@router.delete("/me", status_code=status.HTTP_200_OK)
async def delete_my_account(
    response: Response,
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database),
):
    # Delete own account
    return await delete_my_account_controller(response, current_user, db)


@router.get("/", status_code=status.HTTP_200_OK)
async def admin_list_users(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    _admin: dict = Depends(get_admin_user),
    db: AsyncIOMotorDatabase = Depends(get_database),
):
    # Admin: list all users with pagination
    return await admin_list_users_controller(page, limit, db)


@router.get("/{user_id}", status_code=status.HTTP_200_OK)
async def admin_get_user(
    user_id: str,
    _admin: dict = Depends(get_admin_user),
    db: AsyncIOMotorDatabase = Depends(get_database),
):
    # Admin: get user by ID
    return await admin_get_user_controller(user_id, db)


@router.patch("/{user_id}", status_code=status.HTTP_200_OK)
async def admin_update_user(
    user_id: str,
    payload: AdminUserUpdateRequest,
    _admin: dict = Depends(get_admin_user),
    db: AsyncIOMotorDatabase = Depends(get_database),
):
    # Admin: update user role or status
    return await admin_update_user_controller(user_id, payload, db)


@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
async def admin_delete_user(
    user_id: str,
    _admin: dict = Depends(get_admin_user),
    db: AsyncIOMotorDatabase = Depends(get_database),
):
    # Admin: delete user by ID
    return await admin_delete_user_controller(user_id, db)
