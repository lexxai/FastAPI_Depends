import asyncio
import inspect
from functools import wraps
from typing import AsyncGenerator


# Custom Depends class to simulate FastAPI's Depends mechanism
class Depends:
    def __init__(self, func):
        self.func = func  # Store the dependency function

    async def __call__(self):
        result = self.func()  # Call the dependency function
        # Check if the result is an async generator
        if isinstance(result, AsyncGenerator):
            print("This is an async dependency.")
            # Consume the async generator to get the yielded value
            async for item in result:
                return item  # Return the yielded value from the async generator
        print("This is a sync dependency.")
        return result  # If it's sync, return the result directly


# Custom async dependency resolver function (like FastAPI's Depends)
async def depends(dep_func):
    print("depends core")
    # Simply return the result from the Depends object
    return await dep_func()  # If it's async, await the result


# Custom @app_get decorator to simulate route registration and dependency injection
def app_get(path):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            print("Before route handling")

            # Prepare resolved arguments for dependencies
            resolved_kwargs = {}

            for key, value in kwargs.items():
                if isinstance(value, Depends):  # If the argument is a Depends object
                    # Resolve the dependency
                    resolved_kwargs[key] = await depends(value)
                else:
                    resolved_kwargs[key] = value

            # Call the original function with resolved dependencies
            result = await func(*args, **resolved_kwargs)
            print(f"After route handling with result: {result}")
            return result

        return wrapper

    return decorator


# Simulated async dependency function using yield (async generator)
async def some_dependency():
    print("try to open resource")
    await asyncio.sleep(1)  # Simulate async behavior, e.g., opening a resource
    print("resource opened")
    yield "dependency result"  # Yield the result to simulate dependency injection
    print("closing resource")
    await asyncio.sleep(1)  # Simulate resource cleanup


# Simulated sync dependency function
def sync_dependency():
    return "sync dependency result"


# Route function using our custom decorator and dependency simulation
@app_get("/items/{item_id}")
async def read_item(item_id: int, dep: str):
    return {"item_id": item_id, "dep": dep}


# Simulating a request to the route
async def simulate_request():
    # Using Depends object to wrap dependencies
    print(await read_item(101, dep=Depends(some_dependency)))  # Async dependency
    print(await read_item(102, dep=Depends(sync_dependency)))  # Sync dependency


# Run the simulation
asyncio.run(simulate_request())
