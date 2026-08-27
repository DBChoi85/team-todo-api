from fastapi.testclient import TestClient
from app.main import app, todos

client = TestClient(app)

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
    original_todos = todos.copy()

    try:
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

    finally:
        todos.clear()
        todos.extend(original_todos)