from datetime import datetime, timezone
from database.database import Base
from sqlalchemy import (
    Column, Integer,
    String, Boolean,
    DateTime, Text
)

class Book(Base):
    __tablename__ = 'book'
    id = Column(Integer, primary_key=True)

    title = Column(String(255), nullable=False)
    author = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    price = Column(Integer, nullable=False)
