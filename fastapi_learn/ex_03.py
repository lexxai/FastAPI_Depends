from fastapi import Depends, FastAPI

app = FastAPI()

class DependencyClass:
    def __init__(self):
        self.value = "class_dependency_value"

    def get_value(self):
        return self.value

@app.get("/class")
def read_class_dependency(dependency: DependencyClass = Depends(DependencyClass)):
    return {"class_dependency": dependency.get_value()}

