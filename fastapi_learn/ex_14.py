from contextlib import asynccontextmanager
from fastapi import APIRouter, FastAPI, Depends


if __name__ == "fastapi_learn.ex_14":

    @asynccontextmanager
    async def lifespan(app):
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
