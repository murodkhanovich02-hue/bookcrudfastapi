from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session

from database.session import get_db
from schemas.book import BookCreate

book_router = APIRouter(prefix="/books")

@book_router.post('/create', status_code=status.HTTP_201_CREATED)
async def create_book(book: BookCreate, db: Session = Depends(get_db())):
    pass
