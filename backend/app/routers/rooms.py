from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..auth import require_admin
from ..db import get_db
from ..models import Room
from ..schemas import RoomCreate, RoomResponse, RoomUpdate

router = APIRouter()


@router.get("/rooms", response_model=list[RoomResponse])
def list_rooms(db: Session = Depends(get_db)):
    rooms = db.query(Room).order_by(Room.id.desc()).all()
    return [serialize_room(room) for room in rooms]


@router.get("/rooms/{room_id}", response_model=RoomResponse)
def get_room(room_id: int, db: Session = Depends(get_db)):
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Помещение не найдено")
    return serialize_room(room)


@router.post("/rooms", response_model=RoomResponse, dependencies=[Depends(require_admin)])
def create_room(payload: RoomCreate, db: Session = Depends(get_db)):
    room = Room(
        name=payload.name,
        capacity=payload.capacity,
        description=payload.description,
        equipment="|".join(payload.equipment),
        photo_url=str(payload.photo_url),
    )
    db.add(room)
    db.commit()
    db.refresh(room)
    return serialize_room(room)


@router.put("/rooms/{room_id}", response_model=RoomResponse, dependencies=[Depends(require_admin)])
def update_room(room_id: int, payload: RoomUpdate, db: Session = Depends(get_db)):
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Помещение не найдено")
    room.name = payload.name
    room.capacity = payload.capacity
    room.description = payload.description
    room.equipment = "|".join(payload.equipment)
    room.photo_url = str(payload.photo_url)
    db.commit()
    db.refresh(room)
    return serialize_room(room)


@router.delete("/rooms/{room_id}", dependencies=[Depends(require_admin)])
def delete_room(room_id: int, db: Session = Depends(get_db)):
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Помещение не найдено")
    db.delete(room)
    db.commit()
    return {"deleted": True}


def serialize_room(room: Room):
    return {
        "id": room.id,
        "name": room.name,
        "capacity": room.capacity,
        "description": room.description,
        "equipment": room.equipment.split("|") if room.equipment else [],
        "photo_url": room.photo_url,
    }
