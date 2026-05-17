const API_BASE = "/api";

function authHeaders(token) {
  return token ? { Authorization: `Bearer ${token}` } : {};
}

function translateValidationMessage(message) {
  if (!message || typeof message !== "string") {
    return "";
  }

  const minLengthMatch = message.match(/^String should have at least (\d+) characters?$/);
  if (minLengthMatch) {
    return `Строка должна содержать минимум ${minLengthMatch[1]} символа(ов)`;
  }

  const maxLengthMatch = message.match(/^String should have at most (\d+) characters?$/);
  if (maxLengthMatch) {
    return `Строка должна содержать максимум ${maxLengthMatch[1]} символа(ов)`;
  }

  const greaterThanMatch = message.match(/^Input should be greater than (.+)$/);
  if (greaterThanMatch) {
    return `Значение должно быть больше ${greaterThanMatch[1]}`;
  }

  const lessThanOrEqualMatch = message.match(/^Input should be less than or equal to (.+)$/);
  if (lessThanOrEqualMatch) {
    return `Значение должно быть меньше или равно ${lessThanOrEqualMatch[1]}`;
  }

  if (message.includes("Input should be a valid URL")) {
    return "Введите корректную ссылку (URL)";
  }

  if (message.startsWith("Value error, ")) {
    return message.replace("Value error, ", "");
  }

  return message;
}

function extractErrorMessage(body, fallback) {
  if (!body) {
    return fallback;
  }

  if (typeof body.detail === "string" && body.detail.trim()) {
    return translateValidationMessage(body.detail);
  }

  if (Array.isArray(body.detail)) {
    const combined = body.detail
      .map((item) => {
        if (typeof item === "string") {
          return translateValidationMessage(item);
        }
        if (item && typeof item.msg === "string") {
          return translateValidationMessage(item.msg);
        }
        return "";
      })
      .filter(Boolean)
      .join(". ");
    if (combined) {
      return combined;
    }
  }

  if (typeof body.message === "string" && body.message.trim()) {
    return translateValidationMessage(body.message);
  }

  return fallback;
}

export async function login(username, password) {
  const res = await fetch(`${API_BASE}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password })
  });
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(extractErrorMessage(body, "Не удалось войти в систему"));
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
    throw new Error(extractErrorMessage(body, "Не удалось добавить пользователя"));
  }
  return res.json();
}

export async function fetchRooms() {
  const res = await fetch(`${API_BASE}/rooms/rooms`);
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(extractErrorMessage(body, "Не удалось загрузить помещения"));
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
    throw new Error(extractErrorMessage(body, "Не удалось добавить помещение"));
  }
  return res.json();
}

export async function deleteRoom(roomId, token) {
  const res = await fetch(`${API_BASE}/rooms/rooms/${roomId}`, {
    method: "DELETE",
    headers: {
      ...authHeaders(token)
    }
  });
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(extractErrorMessage(body, "Не удалось удалить помещение"));
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
    throw new Error(extractErrorMessage(body, "Не удалось проверить доступность"));
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
    throw new Error(extractErrorMessage(body, "Не удалось создать бронирование"));
  }
  return res.json();
}

export async function fetchMyBookings(token) {
  const res = await fetch(`${API_BASE}/bookings/bookings/me`, {
    headers: {
      ...authHeaders(token)
    }
  });
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(extractErrorMessage(body, "Не удалось загрузить ваши бронирования"));
  }
  return res.json();
}
