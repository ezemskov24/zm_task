import pytest
from fastapi.testclient import TestClient


@pytest.mark.asyncio
async def test_create_task(client: TestClient, db_session):
    task_data = {
        "task_info": "Test Task",
        "datetime_to_do": "2025-04-01T10:00:00"
    }
    headers = {
        "Authorization": "Bearer test_token"
    }

    response = client.post("/tasks/create", json=task_data, headers=headers)

    assert response.status_code == 200, f"Expected 200 but got {response.status_code}, response: {response.json()}"

    task = response.json()
    assert task["task_info"] == "Test Task"
    assert task["datetime_to_do"] == "2025-04-01T10:00:00"


@pytest.mark.asyncio
async def test_list_tasks(client: TestClient, db_session):
    task_data = {
        "task_info": "Test Task",
        "datetime_to_do": "2025-04-01T10:00:00"
    }
    client.post("/tasks/create", json=task_data, headers={"Authorization": "Bearer test_token"})

    response = client.get("/tasks/list", headers={"Authorization": "Bearer test_token"})

    assert response.status_code == 200, f"Expected 200 but got {response.status_code}, response: {response.json()}"

    tasks = response.json()
    assert len(tasks) > 0, "Expected to find at least one task in the list"


@pytest.mark.asyncio
async def test_get_task(client: TestClient, db_session):
    task_data = {
        "task_info": "Test Task",
        "datetime_to_do": "2025-04-01T10:00:00"
    }
    response_create = client.post("/tasks/create", json=task_data, headers={"Authorization": "Bearer test_token"})
    task_id = response_create.json()["id"]

    response = client.get(f"/tasks/{task_id}", headers={"Authorization": "Bearer test_token"})

    assert response.status_code == 200, f"Expected 200 but got {response.status_code}, response: {response.json()}"

    task = response.json()
    assert task["task_info"] == "Test Task"
    assert task["datetime_to_do"] == "2025-04-01T10:00:00"


@pytest.mark.asyncio
async def test_update_task(client: TestClient, db_session):
    task_data = {
        "task_info": "Test Task",
        "datetime_to_do": "2025-04-01T10:00:00"
    }
    response_create = client.post("/tasks/create", json=task_data, headers={"Authorization": "Bearer test_token"})
    task_id = response_create.json()["id"]

    updated_task_data = {
        "task_info": "Updated Task",
        "datetime_to_do": "2025-05-01T12:00:00"
    }
    response_update = client.patch(f"/tasks/{task_id}/update", json=updated_task_data, headers={"Authorization": "Bearer test_token"})

    assert response_update.status_code == 200, f"Expected 200 but got {response_update.status_code}, response: {response_update.json()}"

    updated_task = response_update.json()
    assert updated_task["task_info"] == "Updated Task"
    assert updated_task["datetime_to_do"] == "2025-05-01T12:00:00"
