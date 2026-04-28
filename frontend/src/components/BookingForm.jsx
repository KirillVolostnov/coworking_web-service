import { useState } from "react";
import { checkAvailability, createBooking } from "../api/client";

function translateBookingMessage(message) {
  if (!message) {
    return "Слот недоступен";
  }

  if (message.includes("Booking cannot exceed 6 hours")) {
    return "Бронирование не может длиться больше 6 часов";
  }

  if (message.includes("Selected time slot is already occupied")) {
    return "Выбранный временной слот уже занят";
  }

  if (message.includes("end_time must be greater than start_time")) {
    return "Время окончания должно быть позже времени начала";
  }

  return message;
}

export default function BookingForm({ roomId, token }) {
  const [start, setStart] = useState("");
  const [end, setEnd] = useState("");
  const [message, setMessage] = useState("");
  const [isError, setIsError] = useState(false);

  async function onCheck() {
    try {
      const response = await checkAvailability({
        room_id: roomId,
        start_time: start,
        end_time: end
      });
      setIsError(!response.available);
      setMessage(response.available ? "Слот свободен" : translateBookingMessage(response.reason));
    } catch (error) {
      setIsError(true);
      setMessage(translateBookingMessage(error.message));
    }
  }

  async function onBook() {
    try {
      await createBooking(
        {
          room_id: roomId,
          start_time: start,
          end_time: end
        },
        token
      );
      setIsError(false);
      setMessage("Бронирование создано");
    } catch (error) {
      setIsError(true);
      setMessage(translateBookingMessage(error.message));
    }
  }

  return (
    <div style={{ marginTop: 12 }}>
      <label>
        Время начала
        <input type="datetime-local" value={start} onChange={(e) => setStart(e.target.value)} />
      </label>
      <label>
        Время окончания
        <input type="datetime-local" value={end} onChange={(e) => setEnd(e.target.value)} />
      </label>
      <div style={{ display: "flex", gap: 8, marginTop: 8 }}>
        <button onClick={onCheck}>Проверить доступность</button>
        <button onClick={onBook}>Забронировать</button>
      </div>
      {message ? <p className={isError ? "error" : "success"}>{message}</p> : null}
    </div>
  );
}
