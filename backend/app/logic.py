from datetime import timedelta

from sqlalchemy.orm import Session

from .models import Booking, Room
from .schemas import BookingRequest

# Максимальная разрешенная длительность бронирования (в часах)
MAX_BOOKING_HOURS = 6


def validate_booking_constraints(db: Session, request: BookingRequest) -> tuple[bool, str | None]:
    """
    Проверяет бизнес-правила перед созданием бронирования.
    Возвращает кортеж (успех, сообщение об ошибке).
    """
    # 0. Проверка существования комнаты
    room = db.query(Room).filter(Room.id == request.room_id).first()
    if not room:
        return False, "Room does not exist"

    # 1. Проверка максимальной длительности бронирования
    duration = request.end_time - request.start_time
    if duration > timedelta(hours=MAX_BOOKING_HOURS):
        return False, "Booking cannot exceed 6 hours"

    # 2. Проверка на пересечение времени (коллизии) с другими бронированиями
    # Пересечение возникает, если старая бронь начинается раньше конца новой, 
    # а заканчивается позже начала новой
    conflict = (
        db.query(Booking)
        .filter(
            Booking.room_id == request.room_id,
            Booking.start_time < request.end_time,
            Booking.end_time > request.start_time,
        )
        .first()
    )
    if conflict:
        return False, "Selected time slot is already occupied"
        
    # Все проверки пройдены успешно
    return True, None
