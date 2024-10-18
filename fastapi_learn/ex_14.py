from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.counter = 0  # Initialize on startup
    print(f"Initialize on startup {app.state.counter=}")
    yield


app = FastAPI(lifespan=lifespan)


class StateDependency:
    def increment(self):
        app.state.counter += 1
        return app.state.counter


@app.get("/state-counter")
def state_counter(dep: StateDependency = Depends(StateDependency)):
    return {"count": dep.increment()}
