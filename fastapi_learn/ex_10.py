from fastapi import Depends, FastAPI

app = FastAPI()

def get_limit():
    return 10

@app.get("/items/")
def read_items(limit: int = Depends(get_limit)):
    return {"limit": limit}
