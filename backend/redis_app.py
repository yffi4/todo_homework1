import redis
from typing import Optional
import json

# Redis connection configuration
redis_client = redis.Redis(
    host='redis',  # This matches the service name in docker-compose
    port=6379,
    db=0, 
    decode_responses=True  # Automatically decode responses to Python strings
)

class RedisService:
    @staticmethod
    def set_key(key: str, value: any, expire_seconds: Optional[int] = None) -> bool:
        """
        Set a key-value pair in Redis
        :param key: Key to set
        :param value: Value to set (will be JSON encoded)
        :param expire_seconds: Optional expiration time in seconds
        :return: True if successful
        """
        try:
            serialized_value = json.dumps(value)
            redis_client.set(key, serialized_value)
            if expire_seconds:
                redis_client.expire(key, expire_seconds)
            return True
        except Exception as e:
            print(f"Error setting Redis key: {e}")
            return False

    @staticmethod
    def get_key(key: str) -> Optional[any]:
        """
        Get a value from Redis by key
        :param key: Key to retrieve
        :return: Deserialized value or None if not found
        """
        try:
            value = redis_client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            print(f"Error getting Redis key: {e}")
            return None

    @staticmethod
    def delete_key(key: str) -> bool:
        """
        Delete a key from Redis
        :param key: Key to delete
        :return: True if successful
        """
        try:
            return bool(redis_client.delete(key))
        except Exception as e:
            print(f"Error deleting Redis key: {e}")
            return False

    @staticmethod
    def set_list(key: str, values: list) -> bool:
        """
        Store a list in Redis
        :param key: Key for the list
        :param values: List of values to store
        :return: True if successful
        """
        try:
            pipeline = redis_client.pipeline()
            pipeline.delete(key)
            if values:
                pipeline.rpush(key, *[json.dumps(v) for v in values])
            pipeline.execute()
            return True
        except Exception as e:
            print(f"Error setting Redis list: {e}")
            return False

    @staticmethod
    def get_list(key: str) -> list:
        """
        Get a list from Redis
        :param key: Key of the list to retrieve
        :return: List of deserialized values
        """
        try:
            values = redis_client.lrange(key, 0, -1)
            return [json.loads(v) for v in values]
        except Exception as e:
            print(f"Error getting Redis list: {e}")
            return []

# Example usage in your FastAPI endpoints:
"""
from .redis import RedisService

@app.get("/cache-example/{item_id}")
async def get_cached_item(item_id: str):
    # Try to get from cache first
    cached_data = RedisService.get_key(f"item:{item_id}")
    if cached_data:
        return cached_data
    
    # If not in cache, get from database
    data = get_item_from_db(item_id)  # Your database query
    
    # Cache the result for 1 hour (3600 seconds)
    RedisService.set_key(f"item:{item_id}", data, expire_seconds=3600)
    
    return data
"""
