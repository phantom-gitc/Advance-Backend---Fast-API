from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded

from app.config import settings
from app.database import close_mongo_connection, connect_to_mongo
from app.limiter import limiter
from app.routes.auth_routes import router as auth_router
from app.routes.user_routes import router as user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: connect to database and build indexes
    await connect_to_mongo()
    yield
    # Shutdown: close database connection
    await close_mongo_connection()


app = FastAPI(title="FastAPI Authentication System", lifespan=lifespan)

# Attach rate limiter
app.state.limiter = limiter

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    # Handle rate limit exceeded
    return JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content={"success": False, "message": "Too many requests. Please slow down."},
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    # Standardize HTTP exceptions
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "message": exc.detail},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Format input validation errors
    errors = [{"field": ".".join(str(l) for l in err["loc"] if l != "body"), "message": err["msg"]} for err in exc.errors()]
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"success": False, "message": "Validation error", "errors": errors},
    )


@app.get("/health", tags=["System"])
async def health_check():
    # Health check endpoint
    return {"success": True, "message": "Service is healthy"}


# Register routes
app.include_router(auth_router)
app.include_router(user_router)
