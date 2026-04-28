import os
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from .auth import (
    create_access_token,
    get_current_claims,
    hash_password,
    require_role,
    verify_password,
)
from .db import Base, engine, get_db
from .models import User
from .schemas import LoginRequest, TokenResponse, UserCreateRequest, UserResponse

@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    seed_default_users()
    yield


app = FastAPI(title="Auth Service", lifespan=lifespan)


def seed_default_users():
    admin_username = os.getenv("ADMIN_USERNAME", "admin")
    admin_password = os.getenv("ADMIN_PASSWORD", "admin123")
    default_username = os.getenv("DEFAULT_USERNAME", "user")
    default_password = os.getenv("DEFAULT_PASSWORD", "user123")
    db = next(get_db())
    try:
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
    finally:
        db.close()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == payload.username).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Неверное имя пользователя или пароль")
    return {"access_token": create_access_token(user.username, user.role)}


@app.post(
    "/users",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_role(["admin"]))],
)
def create_user(payload: UserCreateRequest, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == payload.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким именем уже существует",
        )

    user = User(
        username=payload.username,
        password_hash=hash_password(payload.password),
        role="user",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@app.get("/validate")
def validate(claims: dict = Depends(get_current_claims)):
    return {"valid": True, "claims": claims}
