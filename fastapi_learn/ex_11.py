from fastapi import Depends, FastAPI

app = FastAPI()

class MyDependency:
    def __init__(self):
        self.value = 0  # This value is reset with every new instance

    def increment(self):
        self.value += 1
        return self.value

@app.get("/counter")
def counter(dep: MyDependency = Depends(MyDependency)):
    return {"count": dep.increment()}

