from app.db import get_db
from app.models import Room

db = next(get_db())
room_data = {
    "legacy_names": ["Alpha room", "Переговорная Альфа"],
    "name": "Переговорная Альфа",
    "capacity": 4,
    "description": "Переговорная для небольших встреч и созвонов на 2-4 человека.",
    "equipment": "Маркерная доска|Экран",
    "photo_url": "https://dummyimage.com/800x600/e2e8f0/475569.png&text=Alpha+Room",
}

legacy_names = room_data["legacy_names"]
exists = (
    db.query(Room)
    .filter((Room.photo_url == room_data["photo_url"]) | (Room.name.in_(legacy_names)))
    .first()
)
print("Exists:", exists)
if exists:
    print("Old photo_url:", exists.photo_url)
    exists.photo_url = room_data["photo_url"]
    print("New photo_url:", exists.photo_url)
    db.commit()
    print("Committed")
db.close()