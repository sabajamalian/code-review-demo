import json


def test_create_list(client):
    resp = client.post("/api/lists", json={"name": "Groceries"})
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["name"] == "Groceries"
    assert "id" in data


def test_create_list_missing_name(client):
    resp = client.post("/api/lists", json={})
    assert resp.status_code == 400


def test_create_list_no_body(client):
    resp = client.post("/api/lists", content_type="application/json")
    assert resp.status_code == 400


def test_get_lists_empty(client):
    resp = client.get("/api/lists")
    assert resp.status_code == 200
    assert resp.get_json() == []


def test_get_lists(client):
    client.post("/api/lists", json={"name": "A"})
    client.post("/api/lists", json={"name": "B"})
    resp = client.get("/api/lists")
    assert resp.status_code == 200
    data = resp.get_json()
    assert len(data) == 2


def test_get_list(client):
    create_resp = client.post("/api/lists", json={"name": "Work"})
    list_id = create_resp.get_json()["id"]
    resp = client.get(f"/api/lists/{list_id}")
    assert resp.status_code == 200
    assert resp.get_json()["name"] == "Work"


def test_get_list_not_found(client):
    resp = client.get("/api/lists/999")
    assert resp.status_code == 404


def test_update_list(client):
    create_resp = client.post("/api/lists", json={"name": "Old"})
    list_id = create_resp.get_json()["id"]
    resp = client.put(f"/api/lists/{list_id}", json={"name": "New"})
    assert resp.status_code == 200
    assert resp.get_json()["name"] == "New"


def test_update_list_not_found(client):
    resp = client.put("/api/lists/999", json={"name": "X"})
    assert resp.status_code == 404


def test_update_list_missing_name(client):
    create_resp = client.post("/api/lists", json={"name": "A"})
    list_id = create_resp.get_json()["id"]
    resp = client.put(f"/api/lists/{list_id}", json={})
    assert resp.status_code == 400


def test_delete_list(client):
    create_resp = client.post("/api/lists", json={"name": "Temp"})
    list_id = create_resp.get_json()["id"]
    resp = client.delete(f"/api/lists/{list_id}")
    assert resp.status_code == 200
    # Verify it's gone
    assert client.get(f"/api/lists/{list_id}").status_code == 404


def test_delete_list_not_found(client):
    resp = client.delete("/api/lists/999")
    assert resp.status_code == 404
