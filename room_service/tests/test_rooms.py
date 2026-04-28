import os
from uuid import uuid4

from jose import jwt

os.environ["JWT_SECRET"] = "super-secret-key"
os.environ["JWT_ALGORITHM"] = "HS256"

from app.main import app  # noqa: E402


def admin_token():
    return jwt.encode({"sub": "admin", "role": "admin"}, "super-secret-key", algorithm="HS256")


def test_admin_can_create_room():
    from fastapi.testclient import TestClient

    payload = {
        "name": f"Room-{uuid4().hex[:8]}",
        "capacity": 8,
        "description": "Nice room for negotiations",
        "equipment": ["Projector", "Whiteboard"],
        "photo_url": "https://example.com/room-a.jpg",
    }
    with TestClient(app) as client:
        response = client.post(
            "/rooms",
            json=payload,
            headers={"Authorization": f"Bearer {admin_token()}"},
        )
        assert response.status_code == 200
        assert response.json()["name"] == payload["name"]
