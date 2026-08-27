from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_todos():
    response = client.get("todos")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert data[0]["id"] == 1
    assert data[0]["title"] == "Learn GitHub"
    assert data[0]["completed"] is False
