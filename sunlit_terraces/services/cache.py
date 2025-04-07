import time

_cache = {}


async def memory_cache(key, fetch_fn, ttl=300):
    now = time.time()
    if key in _cache:
        cached_value, timestamp = _cache[key]
        if now - timestamp < ttl:
            return cached_value
    value = await fetch_fn()
    _cache[key] = (value, now)
    return value
