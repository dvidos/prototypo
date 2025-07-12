import redis
import hashlib


redis_client = redis.Redis(host="redis", port=6379, decode_responses=True)


def hash_key(**kwargs) -> str:
    """
    Generates a SHA-256 hash from sorted key=value pairs.

    Example:
        make_key(page=1, size=20, filter="john")
    """
    items = sorted(kwargs.items())  # sort keys for consistent ordering
    key_string = "&".join(f"{k}={v}" for k, v in items)
    return hashlib.sha256(key_string.encode("utf-8")).hexdigest()
