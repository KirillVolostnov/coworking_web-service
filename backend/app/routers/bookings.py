from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..auth import get_current_claims
from ..db import get_db
from ..logic import validate_booking_constraints
from ..models import Booking
from ..schemas import AvailabilityResponse, BookingRequest, BookingResponse

router = APIRouter()


@router.post("/check-availability", response_model=AvailabilityResponse)
def check_availability(payload: BookingRequest, db: Session = Depends(get_db)):
    available, reason = validate_booking_constraints(db, payload)
    return {"available": available, "reason": reason}


@router.post("/bookings", response_model=BookingResponse)
def create_booking(
    payload: BookingRequest,
    claims: dict = Depends(get_current_claims),
    db: Session = Depends(get_db),
):
    available, reason = validate_booking_constraints(db, payload)
    if not available:
        raise HTTPException(status_code=400, detail=reason)
    booking = Booking(
        room_id=payload.room_id,
        username=claims.get("sub", "unknown"),
        start_time=payload.start_time,
        end_time=payload.end_time,
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking


@router.get("/bookings/me", response_model=list[BookingResponse])
def list_my_bookings(
    claims: dict = Depends(get_current_claims),
    db: Session = Depends(get_db),
):
    username = claims.get("sub", "")
    bookings = (
        db.query(Booking)
        .filter(Booking.username == username)
        .order_by(Booking.start_time.asc())
        .all()
    )
    return bookings
