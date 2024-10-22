import asyncio
import importlib.machinery
from pathlib import Path
from fastapi import FastAPI
from contextlib import asynccontextmanager

from .pg_init import pg_init_startup
from .wake import ping_service


async def run_modules_startup(loaded_modules):
    for module in loaded_modules:
        if hasattr(module, "startup"):
            await module.startup()


# Define lifespan context for the FastAPI app
@asynccontextmanager
async def lifespan(app):
    ping_task = asyncio.create_task(
        ping_service()
    )  # Start the periodic ping in the background
    await pg_init_startup()
    app.state.counter = 0  # Initialize some state on startup
    print(f"Initialize on startup {app.state.counter=}")
    yield
    print(f"Clean up on shutdown {app.state.counter=}")
    # Perform any cleanup tasks when the app shuts down
    ping_task.cancel()  # Cancel the ping task on shutdown
    await ping_task  # Wait for the ping task to finish gracefully


app = FastAPI(lifespan=lifespan)

loaded_routes = []
loaded_modules = []

# Automatically find all ex_*.py files and import their routers
module_path = Path(__file__).parent
modules_exclude = []
for file in sorted(module_path.glob("ex_??.py")):
    module_name = file.stem  # Get the file name without extension
    module_id = int(module_name.split("_")[-1])
    if module_id > 23 or module_id in modules_exclude:
        continue
    try:
        # Load the module from the file dynamically using importlib.machinery
        loader = importlib.machinery.SourceFileLoader(module_name, str(file))
        module = loader.load_module()
        loaded_modules.append(module)

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
    finally:
        ...


@app.get("/")
async def root():
    return {"loaded_routes": loaded_routes}


@app.head("/health")
@app.get("/health")
async def health():
    return {"status": "OK"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
