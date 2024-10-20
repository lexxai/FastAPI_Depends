from fastapi import FastAPI, APIRouter


app =  FastAPI()  if __name__ == "__main__" else APIRouter() 

@app.get("/")
async def read_root():
    return {"Hello": "World"}

