"""
Cache Manager for PrepWise Backend
Provides Redis caching functionality with graceful degradation
"""
import os
from typing import Optional
from app.core.logging import logger

try:
    from redis import asyncio as aioredis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    logger.warning("redis package not installed. Caching will be disabled.")


class CacheManager:
    """
    Manages Redis caching with automatic fallback if Redis is unavailable
    """

    def __init__(self):
        self.redis: Optional[aioredis.Redis] = None
        self.enabled = False

    async def connect(self, redis_url: str = None):
        """
        Connect to Redis server

        Args:
            redis_url: Redis connection URL (default: from REDIS_URL env var)
        """
        if not REDIS_AVAILABLE:
            logger.info("Redis package not available - caching disabled")
            return

        try:
            redis_url = redis_url or os.getenv("REDIS_URL", "redis://localhost:6379")
            self.redis = await aioredis.from_url(
                redis_url,
                encoding="utf-8",
                decode_responses=True
            )
            # Test connection
            await self.redis.ping()
            self.enabled = True
            logger.info(f"✅ Redis cache connected: {redis_url}")
        except Exception as e:
            logger.warning(f"⚠️  Redis unavailable: {e}. Running without cache.")
            self.redis = None
            self.enabled = False

    async def get(self, key: str) -> Optional[str]:
        """
        Get value from cache

        Args:
            key: Cache key

        Returns:
            Cached value or None if not found or cache disabled
        """
        if not self.enabled or not self.redis:
            return None

        try:
            return await self.redis.get(key)
        except Exception as e:
            logger.error(f"Cache get error for key {key}: {e}")
            return None

    async def setex(self, key: str, seconds: int, value: str):
        """
        Set value in cache with expiration

        Args:
            key: Cache key
            seconds: TTL in seconds
            value: Value to cache
        """
        if not self.enabled or not self.redis:
            return

        try:
            await self.redis.setex(key, seconds, value)
        except Exception as e:
            logger.error(f"Cache setex error for key {key}: {e}")

    async def delete(self, key: str):
        """
        Delete key from cache

        Args:
            key: Cache key to delete
        """
        if not self.enabled or not self.redis:
            return

        try:
            await self.redis.delete(key)
        except Exception as e:
            logger.error(f"Cache delete error for key {key}: {e}")

    async def close(self):
        """Close Redis connection"""
        if self.redis:
            try:
                await self.redis.close()
                logger.info("Redis connection closed")
            except Exception as e:
                logger.error(f"Error closing Redis connection: {e}")


# Global cache manager instance
cache_manager = CacheManager()
