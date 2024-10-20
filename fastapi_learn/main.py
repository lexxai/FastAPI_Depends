import importlib.machinery
from pathlib import Path
from fastapi import FastAPI
from contextlib import asynccontextmanager


# Define lifespan context for the FastAPI app
@asynccontextmanager
async def lifespan(app):
    app.state.counter = 0  # Initialize some state on startup
    print(f"Initialize on startup {app.state.counter=}")
    yield
    print(f"Clean up on shutdown {app.state.counter=}")
    # Perform any cleanup tasks when the app shuts down


app = FastAPI(lifespan=lifespan)

loaded_routes = []

# Automatically find all ex_*.py files and import their routers
module_path = Path(__file__).parent
for file in sorted(module_path.glob("ex_*.py")):
    module_name = file.stem  # Get the file name without extension
    module_id = int(module_name.split("_")[-1])
    if module_id > 23:
        continue

    # Load the module from the file dynamically using importlib.machinery
    loader = importlib.machinery.SourceFileLoader(module_name, str(file))
    module = loader.load_module()

    # Include the router (assuming the module defines 'app' or 'router')
    if hasattr(module, "app"):
        app.include_router(module.app, prefix=f"/{module_name}")
    elif hasattr(module, "router"):
        app.include_router(module.router, prefix=f"/{module_name}")
    if hasattr(module, "main_app"):
        setattr(module, "main_app", app)

    # Collect all routes defined in the module
    for route in app.routes:
        # Check if the route's path starts with the module's prefix
        if route.path.startswith(f"/{module_name}"):
            loaded_routes.append(route.path)


@app.get("/")
async def root():
    return {"loaded_routes": loaded_routes}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
