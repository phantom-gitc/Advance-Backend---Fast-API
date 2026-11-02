from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ASCENDING

from app.config import settings

client = None
db = None


async def connect_to_mongo():
    # Connect to MongoDB and set up database instance
    global client, db
    client = AsyncIOMotorClient(settings.MONGO_URI)
    db = client[settings.DATABASE_NAME]

    # Create unique index for user email
    await db.users.create_index([("email", ASCENDING)], unique=True)

    # Create indexes and TTL index for refresh sessions (auto-delete expired sessions)
    await db.refresh_sessions.create_index([("token_id", ASCENDING)], unique=True)
    await db.refresh_sessions.create_index([("user_id", ASCENDING)])
    await db.refresh_sessions.create_index([("expires_at", ASCENDING)], expireAfterSeconds=0)


async def close_mongo_connection():
    # Close connection when server shuts down
    global client
    if client:
        client.close()


def get_database():
    # Dependency to get active database instance
    return db
