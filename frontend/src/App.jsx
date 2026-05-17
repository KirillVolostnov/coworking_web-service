import { useEffect, useMemo, useState } from "react";
import AddUserPanel from "./components/AddUserPanel";
import AdminPanel from "./components/AdminPanel";
import RoomCard from "./components/RoomCard";
import RoomDetail from "./components/RoomDetail";
import { fetchMyBookings, fetchRooms, login, deleteRoom } from "./api/client";

function parseJwt(token) {
  if (!token) {
    return {};
  }
  try {
    const base64Payload = token.split(".")[1];
    const normalized = base64Payload.replace(/-/g, "+").replace(/_/g, "/");
    return JSON.parse(window.atob(normalized));
  } catch {
    return {};
  }
}

export default function App() {
  const [rooms, setRooms] = useState([]);
  const [myBookings, setMyBookings] = useState([]);
  const [selectedRoom, setSelectedRoom] = useState(null);
  const [username, setUsername] = useState("user");
  const [password, setPassword] = useState("user123");
  const [token, setToken] = useState(() => localStorage.getItem("token") || "");
  const [authError, setAuthError] = useState("");
  const [roomsError, setRoomsError] = useState("");
  const [isAddUserOpen, setIsAddUserOpen] = useState(false);

  const claims = useMemo(() => parseJwt(token), [token]);
  const isAdmin = claims.role === "admin";

  async function loadRooms() {
    try {
      const data = await fetchRooms();
      setRooms(data);
      setRoomsError("");
      if (selectedRoom) {
        setSelectedRoom(data.find((room) => room.id === selectedRoom.id) || null);
      }
    } catch (error) {
      setRooms([]);
      setRoomsError(error.message);
    }
  }

  async function loadMyBookings() {
    try {
      const bookings = await fetchMyBookings(token);
      setMyBookings(bookings);
    } catch {
      setMyBookings([]);
    }
  }

  useEffect(() => {
    if (token) {
      localStorage.setItem("token", token);
      loadRooms().catch(() => {});
      loadMyBookings().catch(() => {});
    } else {
      localStorage.removeItem("token");
    }
  }, [token]);

  async function onLogin(event) {
    event.preventDefault();
    try {
      const response = await login(username, password);
      setToken(response.access_token);
      setAuthError("");
    } catch (error) {
      setAuthError(error.message);
      setToken("");
    }
  }

  function onLogout() {
    setToken("");
    setSelectedRoom(null);
    setIsAddUserOpen(false);
    setMyBookings([]);
  }

  const roomNamesById = useMemo(
    () => rooms.reduce((map, room) => ({ ...map, [room.id]: room.name }), {}),
    [rooms]
  );

  const dateTimeFormatter = useMemo(
    () =>
      new Intl.DateTimeFormat("ru-RU", {
        day: "2-digit",
        month: "2-digit",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit",
        hour12: false
      }),
    []
  );

  if (!token) {
    return (
      <div className="container">
        <h1>Бронирование переговорных комнат</h1>
        <form className="card" onSubmit={onLogin} style={{ maxWidth: 420, margin: "40px auto" }}>
          <h3>Авторизация</h3>
          <label>
            Имя пользователя
            <input value={username} onChange={(e) => setUsername(e.target.value)} />
          </label>
          <label>
            Пароль
            <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
          </label>
          <button type="submit" style={{ marginTop: 10 }}>
            Войти
          </button>
          {authError ? <p className="error">{authError}</p> : null}
        </form>
      </div>
    );
  }

  return (
    <div className="container">
      <div className="card header-card">
        <div>
          <h1 style={{ margin: 0 }}>Бронирование переговорных комнат</h1>
          <p style={{ margin: "6px 0 0 0" }}>
            Вы вошли как {claims.sub} ({claims.role === "admin" ? "администратор" : "пользователь"})
          </p>
        </div>
        <div className="header-actions">
          {isAdmin ? (
            <button type="button" onClick={() => setIsAddUserOpen((current) => !current)}>
              {isAddUserOpen ? "Скрыть форму" : "Добавить пользователя"}
            </button>
          ) : null}
          <button type="button" className="secondary-button" onClick={onLogout}>
            Выйти
          </button>
        </div>
      </div>

      {isAdmin && isAddUserOpen ? <AddUserPanel token={token} onClose={() => setIsAddUserOpen(false)} /> : null}
      {isAdmin ? <AdminPanel token={token} onCreated={loadRooms} /> : null}

      <h2 style={{ marginTop: 20 }}>Мои бронирования</h2>
      <div className="grid">
        {myBookings.length === 0 ? (
          <div className="card">
            <p style={{ margin: 0 }}>У вас пока нет активных бронирований.</p>
          </div>
        ) : (
          myBookings.map((booking) => (
            <div className="card" key={booking.id}>
              <h3 style={{ marginTop: 0, marginBottom: 8 }}>
                {roomNamesById[booking.room_id] || `Помещение #${booking.room_id}`}
              </h3>
              <p style={{ margin: 0 }}>
                {dateTimeFormatter.format(new Date(booking.start_time))} -{" "}
                {dateTimeFormatter.format(new Date(booking.end_time))}
              </p>
            </div>
          ))
        )}
      </div>

      <h2 style={{ marginTop: 20 }}>Помещения</h2>
      {roomsError ? <p className="error">{roomsError}</p> : null}
      <div className="grid">
        {rooms.map((room) => (
          <RoomCard 
            key={room.id} 
            room={room} 
            onSelect={setSelectedRoom} 
            isAdmin={isAdmin}
            onDelete={async () => {
              if (window.confirm(`Вы уверены, что хотите удалить помещение "${room.name}"?`)) {
                try {
                  await deleteRoom(room.id, token);
                  loadRooms();
                } catch (error) {
                  alert(error.message);
                }
              }
            }}
          />
        ))}
      </div>
      <RoomDetail room={selectedRoom} token={token} onBooked={loadMyBookings} />
    </div>
  );
}
