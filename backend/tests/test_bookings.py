from datetime import datetime, timedelta, timezone

def test_check_availability_success(client):
    now = datetime.now(timezone.utc)
    start_time = now + timedelta(days=1)
    end_time = start_time + timedelta(hours=2)
    
    response = client.post(
        "/api/bookings/check-availability",
        json={
            "room_id": 1,
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["available"] is True

def test_check_availability_room_not_found(client):
    now = datetime.now(timezone.utc)
    start_time = now + timedelta(days=1)
    end_time = start_time + timedelta(hours=2)
    
    response = client.post(
        "/api/bookings/check-availability",
        json={
            "room_id": 999,
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["available"] is False
    assert data["reason"] == "Room does not exist"

def test_create_booking_success(client, user_token):
    now = datetime.now(timezone.utc)
    start_time = now + timedelta(days=1)
    end_time = start_time + timedelta(hours=2)
    
    response = client.post(
        "/api/bookings/bookings",
        json={
            "room_id": 1,
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
        },
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["room_id"] == 1
    assert data["username"] == "user"

def test_create_booking_conflict(client, user_token):
    now = datetime.now(timezone.utc)
    start_time = now + timedelta(days=1)
    end_time = start_time + timedelta(hours=2)
    
    # First booking
    client.post(
        "/api/bookings/bookings",
        json={
            "room_id": 1,
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
        },
        headers={"Authorization": f"Bearer {user_token}"},
    )
    
    # Second booking overlapping
    response = client.post(
        "/api/bookings/bookings",
        json={
            "room_id": 1,
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
        },
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Selected time slot is already occupied"

def test_list_my_bookings(client, user_token):
    now = datetime.now(timezone.utc)
    start_time = now + timedelta(days=2)
    end_time = start_time + timedelta(hours=2)
    
    client.post(
        "/api/bookings/bookings",
        json={
            "room_id": 1,
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
        },
        headers={"Authorization": f"Bearer {user_token}"},
    )
    
    response = client.get(
        "/api/bookings/bookings/me",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["room_id"] == 1
    assert data[0]["username"] == "user"
