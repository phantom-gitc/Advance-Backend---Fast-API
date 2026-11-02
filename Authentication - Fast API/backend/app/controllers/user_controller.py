import math
from datetime import datetime, timezone
from bson import ObjectId
from fastapi import HTTPException, Response, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.models.user_model import serialize_user
from app.schemas.auth_schema import ApiResponse
from app.schemas.user_schema import AdminUserUpdateRequest, UserUpdateRequest
from app.services.auth_service import AuthService
from app.utils.cookies import clear_auth_cookies


async def get_my_profile_controller(current_user: dict):
    # Return current user's profile
    return ApiResponse(message="Profile retrieved", data={"user": current_user})


async def update_my_profile_controller(payload: UserUpdateRequest, current_user: dict, db: AsyncIOMotorDatabase):
    # Update allowed fields for current user
    update_data = {}
    if payload.full_name is not None:
        update_data["full_name"] = payload.full_name.strip()

    if not update_data:
        return ApiResponse(message="No changes made", data={"user": current_user})

    update_data["updated_at"] = datetime.now(timezone.utc)
    updated = await db.users.find_one_and_update(
        {"_id": ObjectId(current_user["id"])},
        {"$set": update_data},
        return_document=True,
    )
    return ApiResponse(message="Profile updated", data={"user": serialize_user(updated)})


async def delete_my_account_controller(response: Response, current_user: dict, db: AsyncIOMotorDatabase):
    # Delete account, revoke sessions, and clear cookies
    user_id = ObjectId(current_user["id"])
    await db.users.delete_one({"_id": user_id})

    auth_service = AuthService(db)
    await auth_service.revoke_all_sessions(user_id)
    clear_auth_cookies(response)
    return ApiResponse(message="Account deleted successfully")


async def admin_list_users_controller(page: int, limit: int, db: AsyncIOMotorDatabase):
    # Paginate all users for admin
    skip = (page - 1) * limit
    total = await db.users.count_documents({})
    pages = math.ceil(total / limit) if total > 0 else 1

    cursor = db.users.find().sort("created_at", -1).skip(skip).limit(limit)
    users = [serialize_user(doc) for doc in await cursor.to_list(length=limit)]

    return ApiResponse(
        message="Users list retrieved",
        data={"total": total, "page": page, "limit": limit, "pages": pages, "users": users},
    )


async def admin_get_user_controller(user_id: str, db: AsyncIOMotorDatabase):
    # Get specific user by ID
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user ID")

    user = await db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return ApiResponse(message="User retrieved", data={"user": serialize_user(user)})


async def admin_update_user_controller(user_id: str, payload: AdminUserUpdateRequest, db: AsyncIOMotorDatabase):
    # Admin update for role, status, or name
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user ID")

    update_fields = {}
    if payload.full_name is not None:
        update_fields["full_name"] = payload.full_name.strip()
    if payload.role is not None:
        update_fields["role"] = payload.role
    if payload.is_active is not None:
        update_fields["is_active"] = payload.is_active

    if not update_fields:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields to update")

    update_fields["updated_at"] = datetime.now(timezone.utc)
    updated = await db.users.find_one_and_update(
        {"_id": ObjectId(user_id)},
        {"$set": update_fields},
        return_document=True,
    )
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # If user was deactivated, revoke all their active sessions
    if payload.is_active is False:
        auth_service = AuthService(db)
        await auth_service.revoke_all_sessions(ObjectId(user_id))

    return ApiResponse(message="User updated successfully", data={"user": serialize_user(updated)})


async def admin_delete_user_controller(user_id: str, db: AsyncIOMotorDatabase):
    # Admin delete user and revoke all sessions
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user ID")

    result = await db.users.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    auth_service = AuthService(db)
    await auth_service.revoke_all_sessions(ObjectId(user_id))
    return ApiResponse(message="User deleted successfully")
