from redis import StrictRedis

redis_client = StrictRedis(decode_responses=True)
