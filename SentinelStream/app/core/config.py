import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "SentinelStream"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://sentinel:sentinelpassword@localhost:5432/sentinelstream")
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    CELERY_BROKER_URL: str = os.getenv("CELERY_BROKER_URL", "amqp://guest:guest@localhost:5672//")
    
    class Config:
        case_sensitive = True

settings = Settings()
