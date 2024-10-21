import os
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


# Async dependency to get the database session
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session  # Pass the session to the route handler
        finally:
            print(f"{__name__} get_db.close")
            await session.close()  # Ensure proper cleanup with await


# Route using the async database session
@app.get("/items")
async def read_items(db: AsyncSession = Depends(get_db)):
    result = await db.execute(text("SELECT * FROM items"))
    items = result.fetchall()
    # Convert SQLAlchemy rows to dicts
    items_dict = [dict(row._mapping) for row in items]
    return {"items": items_dict}
