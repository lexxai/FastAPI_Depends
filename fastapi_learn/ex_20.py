import os
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from fastapi import Depends, FastAPI, APIRouter


# Create an asynchronous engine and session factory
DATABASE_URL = os.getenv("PSQL_URL", "postgresql+asyncpg://fs:123@localhost/fs")
DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")


engine = create_async_engine(DATABASE_URL)
AsyncSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)

app = FastAPI() if __name__.startswith("fastapi_learn.") else APIRouter()


class CustomService:
    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session

    async def do_something(self) -> str:
        return "CustomService.do_something: " + str(type(self.db_session))

    async def do_query(self) -> dict:
        result = await self.db_session.execute(text("SELECT * FROM items"))
        items = result.fetchall()
        # Convert SQLAlchemy rows to dicts
        items_dict = [dict(row._mapping) for row in items]
        return items_dict


async def get_db_client() -> AsyncGenerator:
    async with AsyncSessionLocal() as session:
        try:
            yield session  # Provide the session to be used in a route
        finally:
            print(f"{__name__} get_db.session.close")
            await session.close()  # Explicitly close the session
    print(f"{__name__} get_db_client.AsyncSessionLocal finish")


# Another dependency that uses the async database connection
async def get_custom_service(db_client=Depends(get_db_client)):
    return CustomService(db_client)  # Some custom service that uses the db


# Route using the cascading async dependencies
@app.get("/complex_something")
async def complex_route(service: CustomService = Depends(get_custom_service)):
    data = await service.do_something()
    return {"result": data}


@app.get("/complex_query")
async def complex_route(service: CustomService = Depends(get_custom_service)):
    data = await service.do_query()
    return {"result": data}
