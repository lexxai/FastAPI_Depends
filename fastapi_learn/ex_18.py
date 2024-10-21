import os
import redis
from fastapi import Depends, FastAPI, APIRouter


app = FastAPI() if __name__ == "__main__" else APIRouter()

# First dependency to initialize the Redis client
def get_redis():
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
    client = redis.from_url(redis_url)
    try:
        yield client
    finally:
        client.close()


# Second dependency (cascaded) that depends on the Redis client
def get_redis_dependency(redis_client: redis.Redis = Depends(get_redis)):
    return RedisDependency(redis_client)


class RedisDependency:
    def __init__(self, redis_client):
        self.redis_client = redis_client

    def increment(self):
        return self.redis_client.incr("counter")


# Route with cascading dependencies
@app.get("/redis-counter")
def redis_counter(dep: RedisDependency = Depends(get_redis_dependency)):
    count = dep.increment()
    return {"count": count}
