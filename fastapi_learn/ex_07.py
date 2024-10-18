from fastapi import Depends, FastAPI

app = FastAPI()

async def dependency_with_yield():
    # Setup code: this runs before the route
    print("+++++++ Setting up the resource +++++++++++++++++++++++\n")
    resource = "Resource is ready\n"
    yield resource  # Route will receive this value
    print("******  Cleaning up the resource ***********************\n\n")


@app.get("/error")
async def route_with_error(resource: str = Depends(dependency_with_yield)):
    print("Handling request with resource:", resource)
    raise Exception("Something went wrong!")  # Simulate an error

