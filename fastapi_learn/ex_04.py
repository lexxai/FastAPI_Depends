from fastapi import Depends, FastAPI

app = FastAPI()

async def dependency_with_teardown():
    # Setup: This could be opening a database connection
    connection = "Opened connection"
    yield connection  # Provide the dependency value
    # Teardown: This runs after the response is returned
    print("Closing connection")

@app.get("/teardown")
async def read_with_teardown(connection: str = Depends(dependency_with_teardown)):
    return {"connection": connection}
