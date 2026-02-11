from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# =========================
# BASE
# =========================
class BookBase(BaseModel):
    title: str
    author: str
    description: str
    price: int


# =========================
# CREATE
# =========================
class BookCreate(BookBase):
    pass


# =========================
# UPDATE (hammasi optional)
# =========================
class BookUpdate(BaseModel):
    title: Optional[str]
    author: Optional[str]
    description: Optional[str]
    price: Optional[int]


# =========================
# RESPONSE
# =========================
class BookResponse(BookBase):
    id: int
    owner_id: int
    created_at: datetime

    class Config:
        from_attributes = True  # Pydantic v2
