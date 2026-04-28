from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from .auth import require_admin
from .db import Base, engine, get_db
from .models import Room
from .schemas import RoomCreate, RoomResponse, RoomUpdate

@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    seed_default_rooms()
    yield


app = FastAPI(title="Room Service", lifespan=lifespan)


def seed_default_rooms():
    db = next(get_db())
    default_rooms = [
        {
            "legacy_names": ["Alpha room", "Переговорная Альфа"],
            "name": "Переговорная Альфа",
            "capacity": 4,
            "description": "Переговорная для небольших встреч и созвонов на 2-4 человека.",
            "equipment": "Маркерная доска|Экран",
            "photo_url": "https://images.unsplash.com/photo-1497366216548-37526070297c",
        },
        {
            "legacy_names": ["Beta room", "Переговорная Бета"],
            "name": "Переговорная Бета",
            "capacity": 6,
            "description": "Удобная переговорная для встреч команды и общения с клиентами до 6 человек.",
            "equipment": "Проектор|Маркерная доска|Конференц-телефон",
            "photo_url": "https://images.unsplash.com/photo-1497366811353-6870744d04b2",
        },
        {
            "legacy_names": ["Gamma room", "Переговорная Гамма"],
            "name": "Переговорная Гамма",
            "capacity": 20,
            "description": "Большой зал для презентаций, стратегических сессий и общих обсуждений до 20 человек.",
            "equipment": "Проектор|Маркерная доска|Кондиционер|Видеоконференцсвязь",
            "photo_url": "https://images.unsplash.com/photo-1524758631624-e2822e304c36",
        },
    ]
    try:
        for room_data in default_rooms:
            legacy_names = room_data["legacy_names"]
            exists = (
                db.query(Room)
                .filter((Room.photo_url == room_data["photo_url"]) | (Room.name.in_(legacy_names)))
                .first()
            )
            if not exists:
                db.add(Room(**{key: value for key, value in room_data.items() if key != "legacy_names"}))
            else:
                exists.name = room_data["name"]
                exists.capacity = room_data["capacity"]
                exists.description = room_data["description"]
                exists.equipment = room_data["equipment"]
                exists.photo_url = room_data["photo_url"]
        db.commit()
    finally:
        db.close()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/rooms", response_model=list[RoomResponse])
def list_rooms(db: Session = Depends(get_db)):
    rooms = db.query(Room).order_by(Room.id.desc()).all()
    return [serialize_room(room) for room in rooms]


@app.get("/rooms/{room_id}", response_model=RoomResponse)
def get_room(room_id: int, db: Session = Depends(get_db)):
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Помещение не найдено")
    return serialize_room(room)


@app.post("/rooms", response_model=RoomResponse, dependencies=[Depends(require_admin)])
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


@app.put("/rooms/{room_id}", response_model=RoomResponse, dependencies=[Depends(require_admin)])
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


@app.delete("/rooms/{room_id}", dependencies=[Depends(require_admin)])
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
