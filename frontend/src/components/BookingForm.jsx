import { useState } from "react";
import DatePicker, { registerLocale } from "react-datepicker";
import { ru } from "date-fns/locale";
import { checkAvailability, createBooking } from "../api/client";

registerLocale("ru", ru);

function toApiDateTime(value) {
  const year = value.getFullYear();
  const month = String(value.getMonth() + 1).padStart(2, "0");
  const day = String(value.getDate()).padStart(2, "0");
  const hours = String(value.getHours()).padStart(2, "0");
  const minutes = String(value.getMinutes()).padStart(2, "0");
  return `${year}-${month}-${day}T${hours}:${minutes}`;
}

const DURATION_OPTIONS = Array.from({ length: 18 }, (_, index) => (index + 1) * 20);
const TIME_OPTIONS = Array.from({ length: 29 }, (_, index) => {
  const totalMinutes = (7 * 60) + index * 30;
  const hours = String(Math.floor(totalMinutes / 60)).padStart(2, "0");
  const minutes = String(totalMinutes % 60).padStart(2, "0");
  return `${hours}:${minutes}`;
});

function formatDurationLabel(minutes) {
  const hours = Math.floor(minutes / 60);
  const restMinutes = minutes % 60;

  if (hours === 0) {
    return `${minutes} мин`;
  }
  if (restMinutes === 0) {
    return `${hours} ч`;
  }
  return `${hours} ч ${restMinutes} мин`;
}

function mergeDateAndTime(selectedDate, timeValue) {
  if (!selectedDate || !timeValue) {
    return null;
  }
  const [hoursText, minutesText] = timeValue.split(":");
  const hours = Number(hoursText);
  const minutes = Number(minutesText);
  const merged = new Date(selectedDate);
  merged.setHours(hours, minutes, 0, 0);
  return merged;
}

function buildEndDate(startDate, durationMinutes) {
  if (!startDate || !durationMinutes) {
    return null;
  }
  return new Date(startDate.getTime() + durationMinutes * 60 * 1000);
}

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

export default function BookingForm({ roomId, token, onBooked }) {
  const [selectedDate, setSelectedDate] = useState(null);
  const [startTime, setStartTime] = useState("");
  const [durationMinutes, setDurationMinutes] = useState(60);
  const [message, setMessage] = useState("");
  const [isError, setIsError] = useState(false);

  const start = mergeDateAndTime(selectedDate, startTime);
  const end = buildEndDate(start, durationMinutes);
  const hasSelectedRange = Boolean(selectedDate && startTime && durationMinutes && start && end);

  async function onCheck() {
    if (!hasSelectedRange) {
      setIsError(true);
      setMessage("Выберите дату, время начала и длительность.");
      return;
    }

    try {
      const response = await checkAvailability({
        room_id: roomId,
        start_time: toApiDateTime(start),
        end_time: toApiDateTime(end)
      });
      setIsError(!response.available);
      setMessage(response.available ? "Слот свободен" : translateBookingMessage(response.reason));
    } catch (error) {
      setIsError(true);
      setMessage(translateBookingMessage(error.message));
    }
  }

  async function onBook() {
    if (!hasSelectedRange) {
      setIsError(true);
      setMessage("Выберите дату, время начала и длительность.");
      return;
    }

    try {
      await createBooking(
        {
          room_id: roomId,
          start_time: toApiDateTime(start),
          end_time: toApiDateTime(end)
        },
        token
      );
      setIsError(false);
      setMessage("Бронирование создано");
      if (onBooked) {
        onBooked();
      }
    } catch (error) {
      setIsError(true);
      setMessage(translateBookingMessage(error.message));
    }
  }

  return (
    <div style={{ marginTop: 12 }}>
      <label>
        Дата
        <DatePicker
          selected={selectedDate}
          onChange={(value) => setSelectedDate(value)}
          dateFormat="dd.MM.yyyy"
          minDate={new Date()}
          placeholderText="дд.мм.гггг"
          locale="ru"
          className="date-picker-input"
          calendarStartDay={1}
        />
      </label>
      <label>
        Время начала
        <select value={startTime} onChange={(event) => setStartTime(event.target.value)}>
          <option value="">Выберите время</option>
          {TIME_OPTIONS.map((time) => (
            <option key={time} value={time}>
              {time}
            </option>
          ))}
        </select>
      </label>
      <label>
        Длительность
        <select
          value={durationMinutes}
          onChange={(event) => setDurationMinutes(Number(event.target.value))}
        >
          {DURATION_OPTIONS.map((minutes) => (
            <option key={minutes} value={minutes}>
              {formatDurationLabel(minutes)}
            </option>
          ))}
        </select>
      </label>
      <div style={{ display: "flex", gap: 8, marginTop: 8 }}>
        <button onClick={onCheck}>Проверить доступность</button>
        <button onClick={onBook}>Забронировать</button>
      </div>
      {hasSelectedRange ? (
        <p style={{ marginTop: 10, fontSize: 14 }}>
          Интервал бронирования: {selectedDate ? selectedDate.toLocaleDateString("ru-RU") : ""} {startTime} -{" "}
          {end ? end.toLocaleTimeString("ru-RU", { hour: "2-digit", minute: "2-digit", hour12: false }) : ""}
        </p>
      ) : null}
      {message ? <p className={isError ? "error" : "success"}>{message}</p> : null}
    </div>
  );
}
