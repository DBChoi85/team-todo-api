from fastapi import FastAPI

app = FastAPI(
        title = "Team Todo API",
        version = "0.1.0"
        )

todos = [
        {"id" : 1, "title": "Learn GitHub", "completed": False},
        {"id" : 2, "title": "Build Todo API", "completed": False},
        ]


@app.get("/")
def root():
    return {"message": "Team Todo API"}

@app.get("/todos")
def get_todos():
    return todos
