import redis
from fastapi import FastAPI, Depends

app = FastAPI()


# Dependency to initialize the Redis client
def get_redis():
    print("Opening Redis connection")
    client = redis.Redis(host="localhost", port=6379, db=0)
    try:
        yield client
    finally:
        print("Close Redis connection")
        client.close()  # Optional: Close the connection if necessary


class RedisDependency:
    def __init__(self, redis_client):
        self.redis_client = redis_client

    def increment(self):
        return self.redis_client.incr("counter")


# Route using Redis as a dependency
@app.get("/redis-counter")
def redis_counter(redis_client: redis.Redis = Depends(get_redis)):
    dep = RedisDependency(redis_client)
    try:
        print("Try increment Redis value")
        count = dep.increment()
    except Exception as e:
        message = f"Redis error: {e}"
        print(message)
        return {"error": message}
    return {"count": count}
