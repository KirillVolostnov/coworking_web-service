def test_list_rooms(client):
    response = client.get("/api/rooms/rooms")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 3  # Seeded rooms
    assert data[0]["name"] == "Переговорная Гамма"

def test_get_room(client):
    response = client.get("/api/rooms/rooms/1")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Переговорная Альфа"

def test_create_room_as_admin(client, admin_token):
    response = client.post(
        "/api/rooms/rooms",
        json={
            "name": "Test Room",
            "capacity": 10,
            "description": "A very nice test room",
            "equipment": ["Projector"],
            "photo_url": "https://example.com/photo.jpg"
        },
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Room"
    assert data["capacity"] == 10

def test_create_room_as_user(client, user_token):
    response = client.post(
        "/api/rooms/rooms",
        json={
            "name": "Test Room 2",
            "capacity": 10,
            "description": "A very nice test room",
            "equipment": ["Projector"],
            "photo_url": "https://example.com/photo.jpg"
        },
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert response.status_code == 403

def test_delete_room_as_admin(client, admin_token):
    response = client.delete(
        "/api/rooms/rooms/1",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    assert response.json()["deleted"] is True

    # Verify it's gone
    response = client.get("/api/rooms/rooms/1")
    assert response.status_code == 404
