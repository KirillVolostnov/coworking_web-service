import BookingForm from "./BookingForm";

export default function RoomDetail({ room, token }) {
  if (!room) {
    return null;
  }

  return (
    <div className="card" style={{ marginTop: 16 }}>
      <h2>{room.name}</h2>
      <p>{room.description}</p>
      <p>
        <strong>Оборудование:</strong> {room.equipment.join(", ")}
      </p>
      <BookingForm roomId={room.id} token={token} />
    </div>
  );
}
