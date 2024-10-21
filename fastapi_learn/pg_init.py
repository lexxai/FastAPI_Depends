import os
import asyncpg
from asyncpg import PostgresError
from faker import Faker


# Initialize Faker
fake = Faker()

DATABASE_URL = os.getenv("PSQL_URL", "postgresql://fs:123@localhost/fs")


async def get_db_client():
    try:
        print("pg_init get_db_client opening db")
        client = await asyncpg.connect(DATABASE_URL)
        try:
            yield client
        finally:
            await client.close()  # Ensure async resource cleanup
            print("pg_init get_db_client close db")
    except (PostgresError, ConnectionError) as e:
        print(f"Error connecting to the database: {e}")
        raise  # Optionally, re-raise the exception to propagate it


# CRUD operations
async def create_table(db_client) -> None:
    try:
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
    except PostgresError as e:
        print(f"Error creating table: {e}")
        raise


async def create_item(item: dict, db_client) -> dict:
    try:
        result = await db_client.fetchrow(
            "INSERT INTO items (name, description) VALUES ($1, $2) RETURNING id, name, description",
            item.get("name"),
            item.get("description"),
        )
        return dict(result)
    except PostgresError as e:
        print(f"Error inserting item: {e}")
        raise


async def pg_init_startup():
    print("Startup pg_init")
    try:
        async for db_client in get_db_client():
            await create_table(db_client)
            for _ in range(4):
                # Insert some test items
                name = fake.word()
                description = fake.sentence()
                item = {"name": name, "description": description}
                result = await create_item(item, db_client)
                print(f"pg_init create_item {result=}")
    except (PostgresError, ConnectionError) as e:
        print(f"Database operation failed: {e}")
