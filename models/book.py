from datetime import datetime, timezone
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Text,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from database.database import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)

    title = Column(String(255), nullable=False)
    author = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    price = Column(Integer, nullable=False)

    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
    )

    owner = relationship("User")
