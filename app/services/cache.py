import redis
import json
from typing import Optional, Any
from app.config import settings

class CacheManager:
    def __init__(self):
        try:
            # Parse Redis URL (redis://localhost:6379/0)
            self.client = redis.from_url(settings.REDIS_URL, decode_responses=True)
            self.enabled = True
        except Exception as e:
            print(f"Warning: Failed to connect to Redis: {e}")
            self.client = None
            self.enabled = False

    def get_analysis(self, url: str) -> Optional[dict]:
        """Retrieve cached analysis if available."""
        if not self.enabled or not self.client:
            return None
        
        try:
            key = f"analysis:{url}"
            data = self.client.get(key)
            if data:
                return json.loads(data)
        except Exception as e:
            print(f"Error reading from Redis cache: {e}")
        
        return None

    def set_analysis(self, url: str, data: dict, ttl: int = 3600) -> bool:
        """Store analysis result in cache with a TTL (default 1h)."""
        if not self.enabled or not self.client:
            return False
        
        try:
            key = f"analysis:{url}"
            self.client.setex(key, ttl, json.dumps(data))
            return True
        except Exception as e:
            print(f"Error writing to Redis cache: {e}")
            return False
