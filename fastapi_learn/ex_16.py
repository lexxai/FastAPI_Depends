from fastapi import Depends, FastAPI, APIRouter

app = FastAPI() if __name__ == "__main__" else APIRouter()


class SingletonDependency:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SingletonDependency, cls).__new__(cls)
            cls._instance.value = 0
        return cls._instance

    def increment(self):
        self.value += 1
        return self.value


# Dependency injection function
def get_singleton_dependency() -> SingletonDependency:
    return SingletonDependency()


@app.get("/singleton")
def singleton_counter(dep: SingletonDependency = Depends(get_singleton_dependency)):
    return {"count": dep.increment()}
