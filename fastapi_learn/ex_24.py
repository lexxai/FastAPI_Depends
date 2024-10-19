from functools import wraps


# Custom dependency resolver function (like FastAPI's Depends)
def depends(dep_func):
    print("depends core")
    return dep_func()  # Call the dependency function to resolve it


# Custom @app_get decorator to simulate route registration and dependency injection
def app_get(path):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print("decorator before")
            # Prepare resolved arguments
            resolved_kwargs = {}
            for key, value in kwargs.items():
                if callable(value):  # If the argument is callable (i.e., a dependency)
                    resolved_kwargs[key] = depends(
                        value
                    )  # Call the dependency resolver
                else:
                    resolved_kwargs[key] = value

            # Call the original function with resolved dependencies
            reault = func(*args, **resolved_kwargs)
            print(f"decorator after with {reault=}")
            return reault

        return wrapper

    return decorator


# Simulated dependency function
def some_dependency():
    return "dependency result"


# Route function using our custom decorator and dependency simulation
@app_get("/items/{item_id}")
def read_item(item_id: int, dep: str = depends(some_dependency)):
    return {"item_id": item_id, "dep": dep}


# Simulating a request to the route
print(read_item(101))  # This should now resolve and inject the dependency correctly
