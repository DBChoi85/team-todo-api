from fastapi import FastAPI
from pydantic import BaseModel, field_validator

app = FastAPI(
        title = "Team Todo API",
        version = "0.1.0"
        )

class Todo(BaseModel):
    id: int
    title: str
    completed: bool

class TodoCreate(BaseModel):
    title: str

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Title must not be empty")

        return value

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

@app.post("/todos", response_model=Todo, status_code=201)
def create_todo(todo: TodoCreate):
    new_todo = Todo(id=max(item.id for item in todos) + 1, title=todo.title, completed=False)
    todos.append(new_todo)
    return new_todo