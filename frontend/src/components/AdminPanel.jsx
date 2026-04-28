import { useState } from "react";
import { createRoom } from "../api/client";

const defaultState = {
  name: "",
  capacity: 2,
  description: "",
  equipment: "",
  photo_url: ""
};

export default function AdminPanel({ token, onCreated }) {
  const [form, setForm] = useState(defaultState);
  const [error, setError] = useState("");
  const [successMessage, setSuccessMessage] = useState("");

  async function onSubmit(event) {
    event.preventDefault();
    setError("");
    setSuccessMessage("");
    try {
      await createRoom(
        {
          ...form,
          capacity: Number(form.capacity),
          equipment: form.equipment.split(",").map((item) => item.trim()).filter(Boolean)
        },
        token
      );
      setForm(defaultState);
      onCreated();
      setSuccessMessage("Помещение успешно добавлено.");
    } catch (submitError) {
      setError(submitError.message);
    }
  }

  return (
    <form className="card" onSubmit={onSubmit} style={{ marginTop: 16 }}>
      <h3>Администратор: добавить помещение</h3>
      <label>
        Название
        <input value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} />
      </label>
      <label>
        Вместимость
        <input
          type="number"
          min="1"
          value={form.capacity}
          onChange={(e) => setForm({ ...form, capacity: e.target.value })}
        />
      </label>
      <label>
        Описание
        <textarea
          value={form.description}
          onChange={(e) => setForm({ ...form, description: e.target.value })}
        />
      </label>
      <label>
        Оборудование (через запятую)
        <input
          value={form.equipment}
          onChange={(e) => setForm({ ...form, equipment: e.target.value })}
        />
      </label>
      <label>
        Ссылка на фото
        <input
          value={form.photo_url}
          onChange={(e) => setForm({ ...form, photo_url: e.target.value })}
        />
      </label>
      <button type="submit" style={{ marginTop: 10 }}>
        Добавить помещение
      </button>
      {successMessage ? <p className="success">{successMessage}</p> : null}
      {error ? <p className="error">{error}</p> : null}
    </form>
  );
}
