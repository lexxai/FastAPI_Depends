from fastapi import Depends, FastAPI, APIRouter

app = FastAPI() if __name__ == "__main__" else APIRouter()


def sub_dependency():
    return "sub_dependency_value"


def main_dependency(sub_value: str = Depends(sub_dependency)):
    return f"main_{sub_value}"


@app.get("/sub")
def read_sub_dependency(dependency: str = Depends(main_dependency)):
    return {"dependency": dependency}
