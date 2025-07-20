import redis
from api.utils.config import get_settings

setting = get_settings()

class RedisClient:
    def __init__(self):
        try:
            self.client = redis.Redis(
                host=setting.REDIS_HOST,
                port=setting.REDIS_PORT,
                decode_responses=True  # Decode responses to UTF-8
            )
            # Test the connection
            self.client.ping()
            print("Successfully connected to Redis.")
        except redis.exceptions.ConnectionError as e:
            print(f"Error connecting to Redis: {e}")
            self.client = None

    def get_client(self):
        return self.client

# Create a single instance of the Redis client to be used across the application
redis_client = RedisClient()

def get_redis_client():
    return redis_client.get_client() 