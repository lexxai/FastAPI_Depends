import asyncpg
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from fastapi import FastAPI, Depends


app = FastAPI()


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
    client = await asyncpg.connect(
        user="fs", password="123", database="fs", host="127.0.0.1"
    )
    try:
        yield client
    finally:
        await client.close()  # Ensure async resource cleanup


# Another dependency that uses the async database connection
async def get_custom_service(db_client=Depends(get_db_client)):
    return CustomService(db_client)  # Some custom service that uses the db


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
