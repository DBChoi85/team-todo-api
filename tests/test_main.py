import pytest
from fastapi.testclient import TestClient

from app.main import app, todos

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_todos():
    original_todos = todos.copy()

    yield

    todos.clear()
    todos.extend(original_todos)

def test_get_todos():
    response = client.get("todos")

    assert response.status_code == 200

    data = response.json()
    
    assert isinstance(data, list)
    assert len(data) > 0

    todo = data[0]

    assert "id" in todo
    assert "title" in todo
    assert "completed" in todo

    assert isinstance(todo["id"], int)
    assert isinstance(todo["title"], str)
    assert isinstance(todo["completed"], bool)

def test_create_todo():
    response = client.post("/todos", json={"title": "Prepare lecture"})

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "Prepare lecture"
    assert data["completed"] is False
    assert isinstance(data["id"], int)


def test_create_todo_with_empty_title():
    response = client.post(
        "/todos",
        json={"title": ""}
    )

    assert response.status_code == 422

def test_create_todo_with_blank_title():
    response = client.post(
        "/todos",
        json={"title": "     "}
    )

    assert response.status_code == 422

def test_create_todo():
    response = client.post(
        "/todos",
        json={"title": "Prepare lecture"}
    )

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "Prepare lecture"
    assert data["completed"] is False
    assert isinstance(data["id"], int)

def test_create_todo_when_list_is_empty():
    todos.clear()

    response = client.post(
        "/todos",
        json={"title": "First Todo"}
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] == 1
    assert data["title"] == "First Todo"
    assert data["completed"] is False

def test_update_todo():
    response = client.put(
        "/todos/1",
        json={
            "title": "Learn GitHub Actions",
            "completed": True
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert data["title"] == "Learn GitHub Actions"
    assert data["completed"] is True

def test_update_nonexistent_todo():
    response = client.put(
        "/todos/999",
        json={
            "title": "Unknown Todo",
            "completed": True
        }
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Todo not found"

def test_update_nonexistent_todo():
    response = client.put(
        "/todos/999",
        json={
            "title": "Unknown Todo",
            "completed": True
        }
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Todo not found"

def test_delete_todo():
    todo_id = todos[0].id

    response = client.delete(f"/todos/{todo_id}")

    assert response.status_code == 204
    assert response.content == b""
    assert all(todo.id != todo_id for todo in todos)

def test_delete_nonexistent_todo():
    response = client.delete("/todos/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Todo not found"

def test_ci_failure_demo():
    assert 1 == 2