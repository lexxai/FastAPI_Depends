from fastapi import Depends, FastAPI

app = FastAPI()

# A simple dependency
def get_dependency():
    return "dependency_value"

@app.get("/")
def read_root(dependency_value: str = Depends(get_dependency)):
    return {"dependency": dependency_value}
