from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import create_db_and_tables
from app.routes.items import router as items_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Setup: create database tables on startup
    create_db_and_tables()
    yield
    # Teardown logic (if needed) can go here


app = FastAPI(
    title="Simple CRUD API",
    description="Clean, industry-standard CRUD API built with FastAPI and SQLModel",
    version="1.0.0",
    lifespan=lifespan
)

# Register routes
app.include_router(items_router)


@app.get("/")
def root():
    return {
        "message": "Welcome to the CRUD API",
        "docs_url": "/docs"
    }
