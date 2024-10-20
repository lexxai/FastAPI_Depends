from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, APIRouter


if __name__ == "__main__":

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        app.state.counter = 0  # Initialize on startup
        print(f"Initialize on startup {app.state.counter=}")
        yield

    app = FastAPI(lifespan=lifespan)
else:
    app = APIRouter()
    main_app = None


class StateDependency:
    def increment(self):
        if main_app:
            main_app.state.counter += 1
            return main_app.state.counter
        app.state.counter += 1
        return app.state.counter


@app.get("/state-counter")
def state_counter(dep: StateDependency = Depends(StateDependency)):
    return {"count": dep.increment()}
