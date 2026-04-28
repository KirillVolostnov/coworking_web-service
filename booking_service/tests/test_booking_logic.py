from datetime import UTC, datetime, timedelta

from app.logic import validate_booking_constraints
from app.models import Booking
from app.schemas import BookingRequest


class DummyQuery:
    def __init__(self, value):
        self.value = value

    def filter(self, *args, **kwargs):
        return self

    def first(self):
        return self.value


class DummyDb:
    def __init__(self, existing=None):
        self.existing = existing

    def query(self, _):
        return DummyQuery(self.existing)


def test_rejects_duration_over_6_hours():
    now = datetime.now(UTC)
    req = BookingRequest(
        room_id=1,
        start_time=now,
        end_time=now + timedelta(hours=7),
    )
    ok, reason = validate_booking_constraints(DummyDb(), req)
    assert ok is False
    assert "6 hours" in reason


def test_detects_collision():
    now = datetime.now(UTC)
    req = BookingRequest(
        room_id=1,
        start_time=now,
        end_time=now + timedelta(hours=1),
    )
    conflict = Booking(room_id=1, username="u", start_time=now, end_time=now + timedelta(hours=2))
    ok, reason = validate_booking_constraints(DummyDb(conflict), req)
    assert ok is False
    assert "occupied" in reason
