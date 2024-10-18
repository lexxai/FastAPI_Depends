from fastapi import Depends, FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

