from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.testclient import TestClient
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime, timedelta
import pytest

from app.core.config import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


app = FastAPI()


fake_db = {
    "tasks": [
        {"id": 1, "datetime_to_do": "2025-03-27T10:00:00", "task_info": "Test Task"}
    ]
}


def create_test_token():
    expiration = datetime.utcnow() + timedelta(hours=1)
    return jwt.encode({"sub": "test_user", "exp": expiration}, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["sub"]
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )


@app.get("/tasks/list")
def list_tasks(current_user: str = Depends(get_current_user)):
    return {"tasks": fake_db["tasks"]}


@app.post("/tasks/create")
def create_task(task_data: dict, current_user: str = Depends(get_current_user)):
    task_data["id"] = len(fake_db["tasks"]) + 1
    fake_db["tasks"].append(task_data)
    return {"task": task_data}


@app.get("/tasks/{task_id}")
def get_task(task_id: int, current_user: str = Depends(get_current_user)):
    task = next((task for task in fake_db["tasks"] if task["id"] == task_id), None)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.patch("/tasks/{task_id}/update")
def test_update_task(client, test_token):
    task_id = 2
    updated_task_data = {
        "datetime_to_do": "2025-03-28T10:00:00",
        "task_info": "Updated Task"
    }
    response = client.patch(f"/tasks/{task_id}/update", json=updated_task_data,
                            headers={"Authorization": f"Bearer {test_token}"})

    assert response.status_code == 200
    assert response.json().get("task_info") == updated_task_data["task_info"]


@pytest.fixture
def test_token():
    return create_test_token()

@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client

def test_list_tasks(client, test_token):
    response = client.get("/tasks/list", headers={"Authorization": f"Bearer {test_token}"})
    assert response.status_code == 200
    assert "tasks" in response.json()

def test_create_task(client, test_token):
    task_data = {
        "datetime_to_do": "2025-03-27T12:00:00",
        "task_info": "New Test Task"
    }
    response = client.post("/tasks/create", json=task_data, headers={"Authorization": f"Bearer {test_token}"})
    assert response.status_code == 200
    assert response.json()["task"]["task_info"] == task_data["task_info"]

def test_get_task(client, test_token):
    task_id = 1
    response = client.get(f"/tasks/{task_id}", headers={"Authorization": f"Bearer {test_token}"})
    assert response.status_code == 200
    assert response.json()["task_info"] == "Test Task"