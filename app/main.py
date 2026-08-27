from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator

app = FastAPI(
        title = "Team Todo API",
        version = "0.1.0"
        )

class TodoBase(BaseModel):
    title: str

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("title must not be empty")

        return value


class Todo(TodoBase):
    id: int
    completed: bool


class TodoCreate(TodoBase):
    pass


class TodoUpdate(TodoBase):
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

@app.post("/todos", response_model=Todo, status_code=201)
def create_todo(todo: TodoCreate):
    next_id = max((item.id for item in todos), default=0) + 1
    new_todo = Todo(id=next_id, title=todo.title, completed=False)
    todos.append(new_todo)
    return new_todo

@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, todo: TodoUpdate):
    for index, existing_todo in enumerate(todos):
        if existing_todo.id == todo_id:
            updated_todo = Todo(
                id=todo_id,
                title=todo.title,
                completed=todo.completed
            )

            todos[index] = updated_todo

            return updated_todo

    raise HTTPException(
        status_code=404,
        detail="Todo not found"
    )

@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: int):
    for index, todo in enumerate(todos):
        if todo.id == todo_id:
            todos.pop(index)
            return

    raise HTTPException(
        status_code=404,
        detail="Todo not found"
    )