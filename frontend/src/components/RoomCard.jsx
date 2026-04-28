export default function RoomCard({ room, onSelect }) {
  return (
    <div className="card">
      <img src={room.photo_url} alt={room.name} style={{ width: "100%", borderRadius: 8 }} />
      <h3>{room.name}</h3>
      <p>Вместимость: {room.capacity}</p>
      <button onClick={() => onSelect(room)}>Подробнее</button>
    </div>
  );
}
