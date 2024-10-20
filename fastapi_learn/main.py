import importlib.machinery
from pathlib import Path
from fastapi import FastAPI

app = FastAPI() if __name__ == "__main__" else APIRouter()


# Automatically find all ex_*.py files and import their routers
module_path = Path(__file__).parent
for file in sorted(module_path.glob("ex_*.py")):
    module_name = file.stem  # Get the file name without extension

    # Load the module from the file dynamically using importlib.machinery
    loader = importlib.machinery.SourceFileLoader(module_name, str(file))
    module = loader.load_module()

    # Include the router (assuming the module defines 'app' or 'router')
    if hasattr(module, "app"):
        app.include_router(module.app, prefix=f"/{module_name}")
    elif hasattr(module, "router"):
        app.include_router(module.router, prefix=f"/{module_name}")


@app.get("/")
async def root():
    return {"message": "Main app route"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
