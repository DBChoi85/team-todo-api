from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
        title = "Team Todo API",
        version = "0.1.0"
        )

class Todo(BaseModel):
    id: int
    title: str
    completed: bool

todos = [
        Todo(id=1, title="Learn GitHub", completed=False),
        Todo(id=2, title="Build Todo API", completed=False),
        ]


@app.get("/")
def root():
    return {"message": "Team Todo API"}

@app.get("/todos")
def get_todos():
    return todos
