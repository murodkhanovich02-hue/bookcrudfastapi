from datetime import datetime, timezone

from database.database import Base
from sqlalchemy import (
    Column, Integer,
    String, Boolean,
    DateTime
)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(250), unique=True, nullable=False)
    password = Column(String(250), nullable=False)

    is_staff = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    failed_login_attempts = Column(Integer, default=0)
    blocked_until = Column(DateTime(timezone=True), nullable=True)

    def __repr__(self):
        return f"User username: {self.username}"
