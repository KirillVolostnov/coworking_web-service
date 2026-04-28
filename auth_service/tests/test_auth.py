def test_login_and_validate():
    from fastapi.testclient import TestClient

    from app.main import app

    with TestClient(app) as client:
        login = client.post("/login", json={"username": "admin", "password": "admin123"})
        assert login.status_code == 200
        token = login.json()["access_token"]

        validate = client.get("/validate", headers={"Authorization": f"Bearer {token}"})
        assert validate.status_code == 200
        assert validate.json()["valid"] is True


def test_admin_can_create_user_and_new_user_can_login():
    from fastapi.testclient import TestClient

    from app.main import app

    with TestClient(app) as client:
        admin_login = client.post("/login", json={"username": "admin", "password": "admin123"})
        assert admin_login.status_code == 200
        admin_token = admin_login.json()["access_token"]

        create_user = client.post(
            "/users",
            json={"username": "new_user", "password": "new_password"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert create_user.status_code == 201
        assert create_user.json()["username"] == "new_user"
        assert create_user.json()["role"] == "user"

        user_login = client.post("/login", json={"username": "new_user", "password": "new_password"})
        assert user_login.status_code == 200


def test_non_admin_cannot_create_user():
    from fastapi.testclient import TestClient

    from app.main import app

    with TestClient(app) as client:
        user_login = client.post("/login", json={"username": "user", "password": "user123"})
        assert user_login.status_code == 200
        user_token = user_login.json()["access_token"]

        create_user = client.post(
            "/users",
            json={"username": "blocked_user", "password": "new_password"},
            headers={"Authorization": f"Bearer {user_token}"},
        )
        assert create_user.status_code == 403
