from fastapi import Depends, FastAPI

app = FastAPI() if __name__ == "__main__" else APIRouter()


async def dependency_with_yield():
    try:
        print("+++++++ Setting up the resource +++++++++++++++++++++++\n")
        resource = "Resource is ready\n"
        yield resource
    finally:
        print("******  Cleaning up the resource ***********************\n\n")


@app.get("/error_finally")
async def route_with_error(resource: str = Depends(dependency_with_yield)):
    print("Handling request with resource:", resource)
    raise Exception("Something went wrong!")  # Simulate an error
