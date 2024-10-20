import os
import redis
from fastapi import Depends, FastAPI, APIRouter

app = FastAPI() if __name__ == "__main__" else APIRouter()

redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
r = redis.from_url(redis_url)


class RedisDependency:
    def increment(self):
        return r.incr("counter")


@app.get("/redis-counter")
def redis_counter(dep: RedisDependency = Depends(RedisDependency)):
    count = dep.increment()
    return {"count": count}
