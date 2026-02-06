from fastapi.exceptions import HTTPException
from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timezone, timedelta

from core.logger import logger
from core.jwt import create_access_token, create_refresh_token, decode_token
from core.security import hash_password, verify_password
from models.models import User
from schemas.auth import RegisterModel, LoginModel, RefreshTokenModel
from database.session import get_db

auth_router = APIRouter(prefix="/auth")


# =========================
# REGISTER
# =========================
@auth_router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user: RegisterModel, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        logger.warning(
            f"REGISTER FAILED | username={user.username} | reason=username_exists"
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with that username already exists.",
        )

    if user.password != user.confirm_password:
        logger.warning(
            f"REGISTER FAILED | username={user.username} | reason=password_mismatch"
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password",
        )

    hashed_password = hash_password(user.password)

    new_user = User(
        username=user.username,
        password=hashed_password,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    logger.info(
        f"REGISTER SUCCESS | user_id={new_user.id} | username={new_user.username}"
    )

    return {
        "user_id": new_user.id,
        "username": new_user.username,
        "message": "User created successfully",
    }


# =========================
# LOGIN
# =========================
@auth_router.post("/login", status_code=status.HTTP_200_OK)
def login(user: LoginModel, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()

    if not db_user:
        logger.warning(
            f"LOGIN FAILED | username={user.username} | reason=user_not_found"
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    now = datetime.now(timezone.utc)

    # ACCOUNT BLOCK CHECK
    if db_user.blocked_until and db_user.blocked_until > now:
        seconds_left = int((db_user.blocked_until - now).total_seconds())
        logger.warning(
            f"LOGIN BLOCKED | user_id={db_user.id} | username={db_user.username} | seconds_left={seconds_left}"
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Account blocked. Try again in {seconds_left} seconds.",
        )

    # WRONG PASSWORD
    if not verify_password(user.password, db_user.password):
        db_user.failed_login_attempts += 1

        logger.warning(
            f"LOGIN FAILED | user_id={db_user.id} | username={db_user.username} | attempts={db_user.failed_login_attempts}"
        )

        if db_user.failed_login_attempts >= 3:
            db_user.blocked_until = now + timedelta(minutes=1)
            db_user.failed_login_attempts = 0

            logger.error(
                f"ACCOUNT BLOCKED | user_id={db_user.id} | username={db_user.username} | duration=60s"
            )

        db.commit()

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    # LOGIN SUCCESS → RESET
    db_user.failed_login_attempts = 0
    db_user.blocked_until = None
    db.commit()

    access_token = create_access_token(sub=db_user.id)
    refresh_token = create_refresh_token(sub=db_user.id)

    logger.info(
        f"LOGIN SUCCESS | user_id={db_user.id} | username={db_user.username}"
    )

    return {
        "user": {
            "id": db_user.id,
            "username": db_user.username,
        },
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


# =========================
# REFRESH TOKEN
# =========================
@auth_router.post("/login/refresh", status_code=status.HTTP_200_OK)
def refresh_token(data: RefreshTokenModel, db: Session = Depends(get_db)):
    payload = decode_token(data.refresh_token)

    if payload.get("type") != "refresh":
        logger.warning("REFRESH FAILED | reason=invalid_token_type")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )

    user_id = payload.get("sub")
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        logger.warning(
            f"REFRESH FAILED | user_id={user_id} | reason=user_not_found"
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    new_access_token = create_access_token(sub=user.id)

    logger.info(
        f"REFRESH SUCCESS | user_id={user.id} | username={user.username}"
    )

    return {
        "access_token": new_access_token,
        "token_type": "bearer",
    }
