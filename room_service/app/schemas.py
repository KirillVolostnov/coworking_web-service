from pydantic import BaseModel, Field, HttpUrl, field_validator


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

    class Config:
        from_attributes = True
