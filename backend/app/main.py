import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy.orm import Session

from .auth import hash_password
from .db import Base, engine, get_db
from .models import Room, User
from .routers import auth, bookings, rooms


def seed_default_users(db: Session):
    admin_username = os.getenv("ADMIN_USERNAME", "admin")
    admin_password = os.getenv("ADMIN_PASSWORD", "admin123")
    default_username = os.getenv("DEFAULT_USERNAME", "user")
    default_password = os.getenv("DEFAULT_PASSWORD", "user123")

    admin_exists = db.query(User).filter(User.username == admin_username).first()
    if not admin_exists:
        admin_exists = User(
            username=admin_username,
            password_hash=hash_password(admin_password),
            role="admin",
        )
        db.add(admin_exists)
    else:
        admin_exists.password_hash = hash_password(admin_password)
        admin_exists.role = "admin"

    user_exists = db.query(User).filter(User.username == default_username).first()
    if not user_exists:
        user_exists = User(
            username=default_username,
            password_hash=hash_password(default_password),
            role="user",
        )
        db.add(user_exists)
    else:
        user_exists.password_hash = hash_password(default_password)
        user_exists.role = "user"
    db.commit()


def seed_default_rooms(db: Session):
    default_rooms = [
        {
            "legacy_names": ["Alpha room", "Переговорная Альфа"],
            "name": "Переговорная Альфа",
            "capacity": 4,
            "description": "Переговорная для небольших встреч и созвонов на 2-4 человека.",
            "equipment": "Маркерная доска|Экран",
            "photo_url": "https://avatars.mds.yandex.net/i?id=24d4c0cfc9c09ddf6a0baa1623d2cc69_l-4825382-images-thumbs&n=13",
        },
        {
            "legacy_names": ["Beta room", "Переговорная Бета"],
            "name": "Переговорная Бета",
            "capacity": 6,
            "description": "Удобная переговорная для встреч команды и общения с клиентами до 6 человек.",
            "equipment": "Проектор|Маркерная доска|Конференц-телефон",
            "photo_url": "https://mebel2biz.ru/tmp/45809d8ac049c82e517386bed47ff54af2983c11_optimizm.jpg",
        },
        {
            "legacy_names": ["Gamma room", "Переговорная Гамма"],
            "name": "Переговорная Гамма",
            "capacity": 20,
            "description": "Большой зал для презентаций, стратегических сессий и общих обсуждений до 20 человек.",
            "equipment": "Проектор|Маркерная доска|Кондиционер|Видеоконференцсвязь",
            "photo_url": "https://wtcmoscow.ru/upload/resize_cache/iblock/56c/600_600_1/Zal-S1.jpg",
        },
    ]
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


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    db = next(get_db())
    try:
        seed_default_users(db)
        seed_default_rooms(db)
    finally:
        db.close()
    yield


app = FastAPI(title="Monolithic Backend API", lifespan=lifespan)

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(rooms.router, prefix="/api/rooms", tags=["rooms"])
app.include_router(bookings.router, prefix="/api/bookings", tags=["bookings"])


@app.get("/health")
def health():
    return {"status": "ok"}
