from fastapi import Depends, FastAPI, APIRouter

app = FastAPI() if __name__.startswith("fastapi_learn.") else APIRouter()


# A simple dependency
def get_dependency():
    return "dependency_value"


@app.get("/")
def read_root(dependency_value: str = Depends(get_dependency)):
    return {"dependency": dependency_value}
