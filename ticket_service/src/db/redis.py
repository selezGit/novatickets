from core.config import REDIS_HOST, REDIS_PORT

import redis

redis_handler = redis.StrictRedis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=0,
    decode_responses=True,
)
