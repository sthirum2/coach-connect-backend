from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import init_db
from app.routers import users

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(title="Coach Connect API", lifespan=lifespan)

app.include_router(users.router, prefix="/users", tags=["Users"])

@app.get("/")
def root():
    return {"message": "Coach Connect API is running"}