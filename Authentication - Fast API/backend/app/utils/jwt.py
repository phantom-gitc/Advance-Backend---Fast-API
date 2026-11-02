import hashlib
import uuid
from datetime import datetime, timedelta, timezone
import jwt
from fastapi import HTTPException, status

from app.config import settings


def hash_token(token: str) -> str:
    # Hash token with SHA-256 before saving to database
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def create_access_token(user_id: str) -> str:
    # Create short-lived JWT access token
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": user_id,
        "type": "access",
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp()),
    }
    return jwt.encode(payload, settings.ACCESS_TOKEN_SECRET, algorithm=settings.JWT_ALGORITHM)


def create_refresh_token(user_id: str) -> tuple[str, str, datetime]:
    # Create long-lived JWT refresh token with unique jti id
    now = datetime.now(timezone.utc)
    expire = now + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    token_id = str(uuid.uuid4())
    payload = {
        "sub": user_id,
        "jti": token_id,
        "type": "refresh",
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp()),
    }
    token = jwt.encode(payload, settings.REFRESH_TOKEN_SECRET, algorithm=settings.JWT_ALGORITHM)
    return token, token_id, expire


def verify_access_token(token: str) -> dict:
    # Decode and verify access token
    try:
        payload = jwt.decode(token, settings.ACCESS_TOKEN_SECRET, algorithms=[settings.JWT_ALGORITHM])
        if payload.get("type") != "access":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type")
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Access token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid access token")


def verify_refresh_token(token: str) -> dict:
    # Decode and verify refresh token
    try:
        payload = jwt.decode(token, settings.REFRESH_TOKEN_SECRET, algorithms=[settings.JWT_ALGORITHM])
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type")
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
