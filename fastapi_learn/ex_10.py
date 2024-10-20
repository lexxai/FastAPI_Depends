from fastapi import Depends, FastAPI, APIRouter

app = FastAPI() if __name__ == "__main__" else APIRouter()


def get_limit():
    return 10


@app.get("/items/")
def read_items(limit: int = Depends(get_limit)):
    return {"limit": limit}
