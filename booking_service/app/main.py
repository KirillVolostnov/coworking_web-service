from contextlib import asynccontextmanager

from fastapi import FastAPI

from .api import router as booking_router
from .db import Base, engine

@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="Booking Service", lifespan=lifespan)
app.include_router(booking_router)


@app.get("/health")
def health():
    return {"status": "ok"}
