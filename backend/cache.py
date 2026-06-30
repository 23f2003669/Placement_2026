import redis
import json

# Connect to Redis
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# Cache a value
def cache_set(key, value, timeout=300):
    """Store data in cache for timeout seconds"""
    redis_client.setex(key, timeout, json.dumps(value))

# Get cached value
def cache_get(key):
    """Get data from cache"""
    data = redis_client.get(key)
    if data:
        return json.loads(data)
    return None

# Delete cache
def cache_delete(key):
    """Delete specific cache"""
    redis_client.delete(key)

# Clear all cache
def cache_clear_all():
    """Clear all cache"""
    redis_client.flushdb()