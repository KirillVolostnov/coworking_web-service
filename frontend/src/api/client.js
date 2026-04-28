const API_BASE = "/api";

function authHeaders(token) {
  return token ? { Authorization: `Bearer ${token}` } : {};
}

export async function login(username, password) {
  const res = await fetch(`${API_BASE}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password })
  });
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.detail || "Не удалось войти в систему");
  }
  return res.json();
}

export async function createUser(payload, token) {
  const res = await fetch(`${API_BASE}/auth/users`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...authHeaders(token)
    },
    body: JSON.stringify(payload)
  });
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.detail || "Не удалось добавить пользователя");
  }
  return res.json();
}

export async function fetchRooms() {
  const res = await fetch(`${API_BASE}/rooms/rooms`);
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.detail || "Не удалось загрузить помещения");
  }
  return res.json();
}

export async function createRoom(payload, token) {
  const res = await fetch(`${API_BASE}/rooms/rooms`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...authHeaders(token)
    },
    body: JSON.stringify(payload)
  });
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.detail || "Не удалось добавить помещение");
  }
  return res.json();
}

export async function checkAvailability(payload) {
  const res = await fetch(`${API_BASE}/bookings/check-availability`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.detail || "Не удалось проверить доступность");
  }
  return res.json();
}

export async function createBooking(payload, token) {
  const res = await fetch(`${API_BASE}/bookings/bookings`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...authHeaders(token)
    },
    body: JSON.stringify(payload)
  });
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.detail || "Не удалось создать бронирование");
  }
  return res.json();
}
