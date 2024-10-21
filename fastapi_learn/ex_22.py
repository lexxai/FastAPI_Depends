from fastapi import Depends, FastAPI, APIRouter


app = FastAPI() if __name__ == "__main__" else APIRouter()


def some_dependency():
    return "dependency result"


def some(in_data: str, dep: str = Depends(some_dependency)):
    print(f"Input: {in_data}, Dependency: {dep}")


@app.get("/items/{item_id}")
def read_item(item_id: int):
    some("aaa")  # Dependency will be injected here
    return {"item_id": item_id}
