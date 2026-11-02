from datetime import datetime, timezone
from bson import ObjectId
from fastapi import HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.models.user_model import serialize_user
from app.utils.jwt import create_access_token, create_refresh_token, hash_token, verify_refresh_token
from app.utils.password import hash_password, verify_password


class AuthService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db

    async def register_user(self, full_name: str, email: str, password: str) -> dict:
        # Check if email is already registered
        existing_user = await self.db.users.find_one({"email": email})
        if existing_user:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

        # Create new user document with hashed password
        now = datetime.now(timezone.utc)
        user_doc = {
            "full_name": full_name.strip(),
            "email": email,
            "password_hash": hash_password(password),
            "role": "user",
            "is_active": True,
            "created_at": now,
            "updated_at": now,
        }
        result = await self.db.users.insert_one(user_doc)
        user_doc["_id"] = result.inserted_id
        return serialize_user(user_doc)

    async def login_user(self, email: str, password: str) -> tuple[dict, str, str]:
        # Find user by email
        user = await self.db.users.find_one({"email": email})
        if not user or not verify_password(password, user["password_hash"]):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

        if not user.get("is_active", True):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account is deactivated")

        user_id = str(user["_id"])

        # Generate tokens
        access_token = create_access_token(user_id)
        refresh_token, token_id, expires_at = create_refresh_token(user_id)

        # Save session in database with hashed token
        await self.db.refresh_sessions.insert_one({
            "user_id": user["_id"],
            "token_id": token_id,
            "refresh_token_hash": hash_token(refresh_token),
            "expires_at": expires_at,
            "revoked_at": None,
            "created_at": datetime.now(timezone.utc),
        })

        return serialize_user(user), access_token, refresh_token

    async def refresh_session(self, raw_refresh_token: str | None) -> tuple[dict, str, str]:
        # Validate refresh token exists
        if not raw_refresh_token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token missing")

        # Verify token signature and claims
        payload = verify_refresh_token(raw_refresh_token)
        user_id = payload.get("sub")
        token_id = payload.get("jti")

        # Find session in database
        session = await self.db.refresh_sessions.find_one({"token_id": token_id})
        if not session:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session not found")

        # Reuse detection: if token is already revoked, revoke all sessions for this user
        if session.get("revoked_at") is not None:
            await self.revoke_all_sessions(session["user_id"])
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token revoked. All sessions cleared.")

        # Check token hash match
        if session.get("refresh_token_hash") != hash_token(raw_refresh_token):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

        # Check user account
        user = await self.db.users.find_one({"_id": session["user_id"]})
        if not user or not user.get("is_active", True):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User account is inactive")

        # Invalidate old session (token rotation)
        now = datetime.now(timezone.utc)
        await self.db.refresh_sessions.update_one({"_id": session["_id"]}, {"$set": {"revoked_at": now}})

        # Issue new tokens
        new_access = create_access_token(user_id)
        new_refresh, new_token_id, new_expires = create_refresh_token(user_id)

        # Save new session
        await self.db.refresh_sessions.insert_one({
            "user_id": user["_id"],
            "token_id": new_token_id,
            "refresh_token_hash": hash_token(new_refresh),
            "expires_at": new_expires,
            "revoked_at": None,
            "created_at": now,
        })

        return serialize_user(user), new_access, new_refresh

    async def logout_user(self, raw_refresh_token: str | None):
        # Mark session as revoked on logout
        if not raw_refresh_token:
            return
        try:
            payload = verify_refresh_token(raw_refresh_token)
            token_id = payload.get("jti")
            if token_id:
                await self.db.refresh_sessions.update_one(
                    {"token_id": token_id, "revoked_at": None},
                    {"$set": {"revoked_at": datetime.now(timezone.utc)}},
                )
        except Exception:
            pass

    async def revoke_all_sessions(self, user_id):
        # Revoke all sessions for a specific user
        oid = ObjectId(user_id) if not isinstance(user_id, ObjectId) else user_id
        await self.db.refresh_sessions.update_many(
            {"user_id": oid, "revoked_at": None},
            {"$set": {"revoked_at": datetime.now(timezone.utc)}},
        )
