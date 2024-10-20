from fastapi import Depends, FastAPI

app = FastAPI() if __name__ == "__main__" else APIRouter()


async def dependency_with_yield():
    # Setup code: this runs before the route
    print("Setting up the resource")
    resource = "Resource is ready"
    yield resource  # Route will receive this value

    # Teardown code: this runs after the route completes
    print("Cleaning up the resource")


@app.get("/example_06")
async def read_example(resource: str = Depends(dependency_with_yield)):
    print("Handling request with resource:", resource)
    return {"message": "Request handled"}
