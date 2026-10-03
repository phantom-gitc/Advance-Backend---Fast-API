from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import create_db_and_tables
from routes.reviews import router as reviews_router


# Lifespan Manager : To manage application start and shutdown 


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    print("Server Started : Database Created")
    yield
    print("Server Stopped : Database Connection Closed")


# Create Application Instance  

app = FastAPI(
    title="Rangmanch API",
    description="Review and Rate Plays",
    version="1.0.0",
    lifespan=lifespan
)



# Include Routers
app.include_router(reviews_router)


@app.get("/")
def read_root():
    return {"message": "Welcome to Rangmanch API"}