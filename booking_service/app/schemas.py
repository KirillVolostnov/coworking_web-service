from datetime import datetime

from pydantic import BaseModel, Field, model_validator


class BookingRequest(BaseModel):
    room_id: int = Field(gt=0)
    start_time: datetime
    end_time: datetime

    @model_validator(mode="after")
    def validate_range(self):
        if self.end_time <= self.start_time:
            raise ValueError("Время окончания должно быть позже времени начала")
        return self


class AvailabilityResponse(BaseModel):
    available: bool
    reason: str | None = None


class BookingResponse(BaseModel):
    id: int
    room_id: int
    username: str
    start_time: datetime
    end_time: datetime

    class Config:
        from_attributes = True
