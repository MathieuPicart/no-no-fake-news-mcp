import time
from fastapi import HTTPException, status, Request
from app.config import settings
from app.services.cache import CacheManager

cache = CacheManager()

async def rate_limiter(request: Request, api_key: str):
    """
    Simple Rate Limiter using Redis.
    Limits by API Key.
    """
    if not api_key:
        return # Should be handled by auth dependency

    # Key for Redis: ratelimit:key:minute_timestamp
    minute = int(time.time() / 60)
    redis_key = f"ratelimit:{api_key}:{minute}"
    
    try:
        current_count = cache.client.get(redis_key)
        if current_count and int(current_count) >= settings.RATE_LIMIT_PER_MINUTE:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Rate limit exceeded. Max {settings.RATE_LIMIT_PER_MINUTE} requests per minute.",
            )
        
        # Increment and set expiry if new
        pipe = cache.client.pipeline()
        pipe.incr(redis_key)
        pipe.expire(redis_key, 60)
        pipe.execute()
        
    except Exception as e:
        # Fallback: if Redis is down, we allow the request but log the error
        print(f"Rate limiter error (Redis): {e}")
        pass
