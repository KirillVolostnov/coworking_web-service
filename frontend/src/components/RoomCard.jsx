export default function RoomCard({ room, onSelect, isAdmin, onDelete }) {
  return (
    <div className="card">
      <img src={room.photo_url} alt={room.name} style={{ width: "100%", borderRadius: 8 }} />
      <h3>{room.name}</h3>
      <p>Вместимость: {room.capacity}</p>
      <div style={{ display: "flex", gap: "8px" }}>
        <button onClick={() => onSelect(room)}>Подробнее</button>
        {isAdmin && (
          <button 
            onClick={onDelete} 
            style={{ backgroundColor: "#dc3545", color: "white", border: "none" }}
          >
            Удалить
          </button>
        )}
      </div>
    </div>
  );
}
