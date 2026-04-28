from datetime import timedelta

from sqlalchemy.orm import Session

from .models import Booking
from .schemas import BookingRequest

MAX_BOOKING_HOURS = 6


def validate_booking_constraints(db: Session, request: BookingRequest) -> tuple[bool, str | None]:
    duration = request.end_time - request.start_time
    if duration > timedelta(hours=MAX_BOOKING_HOURS):
        return False, "Booking cannot exceed 6 hours"

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
    return True, None
