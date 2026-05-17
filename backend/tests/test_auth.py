def test_login_success(client):
    response = client.post(
        "/api/auth/login",
        json={"username": "user", "password": "user123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_failure(client):
    response = client.post(
        "/api/auth/login",
        json={"username": "user", "password": "wrongpassword"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Неверное имя пользователя или пароль"

def test_create_user_as_admin(client, admin_token):
    response = client.post(
        "/api/auth/users",
        json={"username": "newuser", "password": "newpassword123"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "newuser"
    assert data["role"] == "user"
    assert "id" in data

def test_create_user_as_user(client, user_token):
    response = client.post(
        "/api/auth/users",
        json={"username": "newuser2", "password": "newpassword123"},
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Insufficient role permissions"
