from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.config import settings
from app.api.endpoints import router as transaction_router
from app.db.session import engine
from app.db.models import Base
import logging

logging.basicConfig(level=logging.INFO)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup (in production run migrations with Alembic!)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()

app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)

app.include_router(transaction_router, prefix="/api/v1")

@app.get("/health")
async def health_check():
    return {"status": "ok"}

