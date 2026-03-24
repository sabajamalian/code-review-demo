def _create_list(client, name="Test List"):
    resp = client.post("/api/lists", json={"name": name})
    return resp.get_json()["id"]


def test_create_task(client):
    list_id = _create_list(client)
    resp = client.post(f"/api/lists/{list_id}/tasks", json={"title": "Buy milk"})
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["title"] == "Buy milk"
    assert data["completed"] is False
    assert data["list_id"] == list_id


def test_create_task_with_description(client):
    list_id = _create_list(client)
    resp = client.post(
        f"/api/lists/{list_id}/tasks",
        json={"title": "Read book", "description": "Chapter 3"},
    )
    assert resp.status_code == 201
    assert resp.get_json()["description"] == "Chapter 3"


def test_create_task_missing_title(client):
    list_id = _create_list(client)
    resp = client.post(f"/api/lists/{list_id}/tasks", json={})
    assert resp.status_code == 400


def test_create_task_list_not_found(client):
    resp = client.post("/api/lists/999/tasks", json={"title": "X"})
    assert resp.status_code == 404


def test_get_tasks(client):
    list_id = _create_list(client)
    client.post(f"/api/lists/{list_id}/tasks", json={"title": "A"})
    client.post(f"/api/lists/{list_id}/tasks", json={"title": "B"})
    resp = client.get(f"/api/lists/{list_id}/tasks")
    assert resp.status_code == 200
    assert len(resp.get_json()) == 2


def test_get_tasks_list_not_found(client):
    resp = client.get("/api/lists/999/tasks")
    assert resp.status_code == 404


def test_get_task(client):
    list_id = _create_list(client)
    create_resp = client.post(f"/api/lists/{list_id}/tasks", json={"title": "Do it"})
    task_id = create_resp.get_json()["id"]
    resp = client.get(f"/api/lists/{list_id}/tasks/{task_id}")
    assert resp.status_code == 200
    assert resp.get_json()["title"] == "Do it"


def test_get_task_not_found(client):
    list_id = _create_list(client)
    resp = client.get(f"/api/lists/{list_id}/tasks/999")
    assert resp.status_code == 404


def test_update_task(client):
    list_id = _create_list(client)
    create_resp = client.post(f"/api/lists/{list_id}/tasks", json={"title": "Old"})
    task_id = create_resp.get_json()["id"]
    resp = client.put(
        f"/api/lists/{list_id}/tasks/{task_id}",
        json={"title": "New", "completed": True},
    )
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["title"] == "New"
    assert data["completed"] is True


def test_update_task_not_found(client):
    list_id = _create_list(client)
    resp = client.put(f"/api/lists/{list_id}/tasks/999", json={"title": "X"})
    assert resp.status_code == 404


def test_delete_task(client):
    list_id = _create_list(client)
    create_resp = client.post(f"/api/lists/{list_id}/tasks", json={"title": "Gone"})
    task_id = create_resp.get_json()["id"]
    resp = client.delete(f"/api/lists/{list_id}/tasks/{task_id}")
    assert resp.status_code == 200
    assert client.get(f"/api/lists/{list_id}/tasks/{task_id}").status_code == 404


def test_delete_task_not_found(client):
    list_id = _create_list(client)
    resp = client.delete(f"/api/lists/{list_id}/tasks/999")
    assert resp.status_code == 404


def test_cascade_delete_list_removes_tasks(client):
    list_id = _create_list(client)
    client.post(f"/api/lists/{list_id}/tasks", json={"title": "Task 1"})
    client.post(f"/api/lists/{list_id}/tasks", json={"title": "Task 2"})
    # Delete the parent list
    resp = client.delete(f"/api/lists/{list_id}")
    assert resp.status_code == 200
    # List is gone
    assert client.get(f"/api/lists/{list_id}").status_code == 404


def test_task_wrong_list(client):
    """A task from list A should not be accessible under list B."""
    list_a = _create_list(client, "A")
    list_b = _create_list(client, "B")
    create_resp = client.post(f"/api/lists/{list_a}/tasks", json={"title": "Only A"})
    task_id = create_resp.get_json()["id"]
    # Access under wrong list
    resp = client.get(f"/api/lists/{list_b}/tasks/{task_id}")
    assert resp.status_code == 404
