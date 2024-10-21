from contextlib import asynccontextmanager
import os
import asyncpg
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from fastapi import Depends, FastAPI, APIRouter


DATABASE_URL = os.getenv("PSQL_URL", "postgresql://fs:123@127.0.0.1/fs")

if __name__ == "fastapi_learn.ex_21":

    @asynccontextmanager
    async def lifespan(app):
        await startup()
        print(f"Initialize on startup {app.state.counter=}")
        yield

    app = FastAPI(lifespan=lifespan)
else:
    app = APIRouter()
    main_app = None


class CustomService:
    def __init__(self, db_client) -> None:
        self.db_client = db_client

    async def do_something(self) -> str:
        return "CustomService.do_something: " + str(type(self.db_client))

    async def do_query(self) -> dict:
        result = await self.db_client.fetch("SELECT * FROM items")
        items_dict = [dict(record) for record in result]
        return items_dict


async def get_db_client():
    client = await asyncpg.connect(DATABASE_URL)
    try:
        yield client
    finally:
        await client.close()  # Ensure async resource cleanup


# Another dependency that uses the async database connection
async def get_custom_service(db_client=Depends(get_db_client)):
    return CustomService(db_client)  # Some custom service that uses the db


# CRUD ...
async def create_table(db_client) -> None:
    await db_client.execute(
        """
        CREATE TABLE IF NOT EXISTS items (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            description TEXT
        )
    """
    )
    print("Table created successfully or already exists.")


async def create_item(item: dict, db_client) -> dict:
    result = await db_client.fetchrow(
        "INSERT INTO items (name, description) VALUES ($1, $2) RETURNING id, name, description",
        item.get("name"),
        item.get("description"),
    )
    return dict(result)


async def startup():
    print("Startup ex_21")
    await create_table(db_client=Depends(get_db_client))
    item = {"name": "name1", "description": "description1"}
    await create_item(item, db_client=Depends(get_db_client))
    item = {"name": "name2", "description": "description2"}
    await create_item(item, db_client=Depends(get_db_client))


# Route using the cascading async dependencies
@app.get("/complex_something")
async def complex_route(service: CustomService = Depends(get_custom_service)):
    data = await service.do_something()
    result = {"result": data}
    return result


@app.get("/complex_query")
async def complex_route(service: CustomService = Depends(get_custom_service)):
    data = await service.do_query()
    result = {"result": data}
    return result
