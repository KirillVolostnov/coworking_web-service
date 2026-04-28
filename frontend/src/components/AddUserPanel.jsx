import { useState } from "react";
import { createUser } from "../api/client";

const defaultState = {
  username: "",
  password: ""
};

export default function AddUserPanel({ token, onClose }) {
  const [form, setForm] = useState(defaultState);
  const [error, setError] = useState("");
  const [successMessage, setSuccessMessage] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function onSubmit(event) {
    event.preventDefault();
    setIsSubmitting(true);
    setError("");
    setSuccessMessage("");

    try {
      const createdUser = await createUser(form, token);
      setSuccessMessage(`Пользователь ${createdUser.username} успешно добавлен.`);
      setForm(defaultState);
    } catch (submitError) {
      setError(submitError.message);
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <div className="card popup-panel">
      <div className="popup-panel__header">
        <h3 style={{ margin: 0 }}>Добавить пользователя</h3>
        <button type="button" className="secondary-button" onClick={onClose}>
          Закрыть
        </button>
      </div>

      <form onSubmit={onSubmit}>
        <label>
          Имя пользователя
          <input
            value={form.username}
            onChange={(e) => setForm({ ...form, username: e.target.value })}
            placeholder="Например, ivan"
          />
        </label>
        <label>
          Пароль
          <input
            type="password"
            value={form.password}
            onChange={(e) => setForm({ ...form, password: e.target.value })}
            placeholder="Минимум 4 символа"
          />
        </label>
        <button type="submit" style={{ marginTop: 10 }} disabled={isSubmitting}>
          {isSubmitting ? "Добавление..." : "Сохранить пользователя"}
        </button>
        {successMessage ? <p className="success">{successMessage}</p> : null}
        {error ? <p className="error">{error}</p> : null}
      </form>
    </div>
  );
}
