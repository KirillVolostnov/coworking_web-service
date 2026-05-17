from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, field_validator, model_validator


# --- Auth Schemas ---
class LoginRequest(BaseModel):
    username: str = Field(min_length=3, max_length=100)
    password: str = Field(min_length=4, max_length=128)


class UserCreateRequest(BaseModel):
    username: str = Field(min_length=3, max_length=100)
    password: str = Field(min_length=4, max_length=128)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: int
    username: str
    role: str

    model_config = ConfigDict(from_attributes=True)


# --- Room Schemas ---
class RoomBase(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    capacity: int = Field(gt=0, le=500)
    description: str = Field(min_length=5, max_length=2000)
    equipment: list[str] = Field(default_factory=list)
    photo_url: HttpUrl

    @field_validator("equipment")
    @classmethod
    def validate_equipment(cls, value: list[str]) -> list[str]:
        normalized = [item.strip() for item in value if item.strip()]
        if len(normalized) != len(value):
            raise ValueError("Список оборудования не должен содержать пустые значения")
        return normalized


class RoomCreate(RoomBase):
    pass


class RoomUpdate(RoomBase):
    pass


class RoomResponse(RoomBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# --- Booking Schemas ---
class BookingRequest(BaseModel):
    room_id: int = Field(gt=0)
    start_time: datetime
    end_time: datetime

    @model_validator(mode="after")
    def validate_range(self):
        if self.end_time <= self.start_time:
            raise ValueError("end_time must be greater than start_time")
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

    model_config = ConfigDict(from_attributes=True)
