import redis.asyncio as redis
from fastapi import Request
import json
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)

async def check_idempotency(idempotency_key: str):
    if not idempotency_key:
        return None
        
    try:
        cached_response = await redis_client.get(f"idempotency:{idempotency_key}")
        if cached_response:
            return json.loads(cached_response)
    except Exception as e:
        logger.error(f"Redis error during idempotency check: {e}")
        
    return None

async def save_idempotency_response(idempotency_key: str, response_data: dict, expiry: int = 86400):
    if not idempotency_key:
        return
        
    try:
        await redis_client.setex(
            f"idempotency:{idempotency_key}",
            expiry,
            json.dumps(response_data)
        )
    except Exception as e:
        logger.error(f"Redis error during idempotency save: {e}")
