from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session

from database.session import get_db
from models.book import Book
from schemas.book import BookCreate, BookResponse
from deps.auth import get_current_user
from models.user import User

book_router = APIRouter(prefix="/books", tags=["Books"])


# ======================
# PUBLIC LIST (LOGIN SHART EMAS)
# ======================
@book_router.get("/", response_model=list[BookResponse])
def list_books(db: Session = Depends(get_db)):
    return db.query(Book).all()


# ======================
# CREATE (LOGIN SHART)
# ======================
@book_router.post("/create", status_code=status.HTTP_201_CREATED)
def create_book(
    book: BookCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    new_book = Book(
        title=book.title,
        author=book.author,
        owner_id=current_user.id,
    )

    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    return new_book


# ======================
# USER OWN BOOKS
# ======================
@book_router.get("/my", response_model=list[BookResponse])
def my_books(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return db.query(Book).filter(Book.owner_id == current_user.id).all()


# ======================
# UPDATE (FAKAT O‘ZINIKI)
# ======================
@book_router.put("/{book_id}")
def update_book(
    book_id: int,
    book: BookCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_book = db.query(Book).filter(Book.id == book_id).first()

    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")

    if db_book.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    db_book.title = book.title
    db_book.author = book.author

    db.commit()
    db.refresh(db_book)

    return db_book


# ======================
# DELETE (FAKAT O‘ZINIKI)
# ======================
@book_router.delete("/{book_id}")
def delete_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_book = db.query(Book).filter(Book.id == book_id).first()

    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")

    if db_book.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    db.delete(db_book)
    db.commit()

    return {"message": "Book deleted successfully"}
