from fastapi.testclient import TestClient
from app.main import app

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

