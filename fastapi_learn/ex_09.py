from fastapi import Depends, FastAPI, APIRouter

app = FastAPI() if __name__ == "__main__" else APIRouter()


async def dependency_with_yield():
    try:
        # Setup: Open a database connection or similar resource
        print("+++++++ Opening database connection ++++++++++++++++++")
        db_connection = "Database connection"
        yield db_connection  # Pass resource to route
    finally:
        # Cleanup: Close the database connection
        print("****** Closing database connection ******************")


@app.get("/items/")
async def get_items(db=Depends(dependency_with_yield)):
    print("Using resource:", db)
    return {"message": "Success"}
