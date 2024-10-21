from fastapi import FastAPI, APIRouter


app = FastAPI() if __name__.startswith("fastapi_learn.") else APIRouter()


@app.get("/")
async def read_root():
    return {"Hello": "World"}
