from fastapi import Depends, FastAPI, APIRouter

app = FastAPI() if __name__ == "__main__" else APIRouter()


# A simple dependency
def get_dependency():
    return "dependency_value"


@app.get("/")
def read_root(dependency_value: str = Depends(get_dependency)):
    return {"dependency": dependency_value}
