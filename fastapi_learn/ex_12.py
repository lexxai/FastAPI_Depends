from fastapi import Depends, FastAPI

app = FastAPI()

# Global state stored outside the dependency
class GlobalCounter:
    count = 0

class MyDependency:
    def increment(self):
        GlobalCounter.count += 1
        return GlobalCounter.count

@app.get("/global-counter")
def global_counter(dep: MyDependency = Depends(MyDependency)):
    return {"count": dep.increment()}
