import redis.asyncio as redis
from functools import wraps

redis_client = redis.from_url("redis://localhost:6379", encoding="utf-8", decode_responses=True)


def cache(expire: int = 60):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            key = f"{func.__name__}:{args}:{kwargs}"
            cached_data = await redis_client.get(key)
            if cached_data:
                return eval(cached_data)
            result = await func(*args, **kwargs)
            await redis_client.set(key, str(result), ex=expire)
            return result
        return wrapper
    return decorator
