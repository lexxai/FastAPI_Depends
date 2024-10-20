import redis
from fastapi import Depends, FastAPI, APIRouter

app = FastAPI() if __name__ == "__main__" else APIRouter()

r = redis.Redis(host="localhost", port=6379, db=0)


class RedisDependency:
    def increment(self):
        return r.incr("counter")


@app.get("/redis-counter")
def redis_counter(dep: RedisDependency = Depends(RedisDependency)):
    count = dep.increment()
    return {"count": count}
