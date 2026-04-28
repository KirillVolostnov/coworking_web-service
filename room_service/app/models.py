from sqlalchemy import Column, Integer, String, Text

from .db import Base


class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False, unique=True)
    capacity = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)
    equipment = Column(Text, nullable=False, default="")
    photo_url = Column(String(255), nullable=False, default="")
