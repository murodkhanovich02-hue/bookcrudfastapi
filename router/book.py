from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session

from database.session import get_db
from models.book import Book
from models.user import User
from schemas.book import BookCreate, BookUpdate, BookResponse
from deps.auth import get_current_user
from core.logger import book_logger


book_router = APIRouter(
    prefix="/books",
    tags=["Books"]
)


# ==========================================
# PUBLIC LIST (LOGIN SHART EMAS)
# ==========================================
@book_router.get("/", response_model=list[BookResponse])
def list_books(db: Session = Depends(get_db)):
    return db.query(Book).all()


# ==========================================
# CREATE BOOK (LOGIN SHART)
# ==========================================
@book_router.post("/create", status_code=status.HTTP_201_CREATED, response_model=BookResponse)
def create_book(
    book: BookCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    new_book = Book(
        title=book.title,
        author=book.author,
        description=book.description,
        price=book.price,
        owner_id=current_user.id,
    )

    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    book_logger.info(
        f"BOOK CREATED | user_id={current_user.id} | book_id={new_book.id}"
    )

    return new_book


# ==========================================
# USER OWN BOOKS
# ==========================================
@book_router.get("/my-book", response_model=list[BookResponse])
def my_books(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return db.query(Book).filter(Book.owner_id == current_user.id).all()


# ==========================================
# GET SINGLE OWN BOOK
# ==========================================
@book_router.get("/my-book/{book_id}", response_model=BookResponse)
def get_single_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_book = db.query(Book).filter(Book.id == book_id).first()

    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")

    if db_book.owner_id != current_user.id:
        book_logger.error(
            f"BOOK ACCESS DENIED | user_id={current_user.id} | book_id={book_id}"
        )
        raise HTTPException(status_code=403, detail="Not allowed")

    return db_book


# ==========================================
# UPDATE OWN BOOK
# ==========================================
@book_router.put("/my-book/{book_id}", response_model=BookResponse)
def update_book(
    book_id: int,
    book_data: BookUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_book = db.query(Book).filter(Book.id == book_id).first()

    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")

    if db_book.owner_id != current_user.id:
        book_logger.error(
            f"BOOK UPDATE DENIED | user_id={current_user.id} | book_id={book_id}"
        )
        raise HTTPException(status_code=403, detail="Not allowed")

    # Partial update
    if book_data.title is not None:
        db_book.title = book_data.title

    if book_data.author is not None:
        db_book.author = book_data.author

    if book_data.description is not None:
        db_book.description = book_data.description

    if book_data.price is not None:
        db_book.price = book_data.price

    db.commit()
    db.refresh(db_book)

    book_logger.info(
        f"BOOK UPDATED | user_id={current_user.id} | book_id={db_book.id}"
    )

    return db_book


# ==========================================
# DELETE OWN BOOK
# ==========================================
@book_router.delete("/my/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_book = db.query(Book).filter(Book.id == book_id).first()

    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")

    if db_book.owner_id != current_user.id:
        book_logger.error(
            f"BOOK DELETE DENIED | user_id={current_user.id} | book_id={book_id}"
        )
        raise HTTPException(status_code=403, detail="Not allowed")

    db.delete(db_book)
    db.commit()

    book_logger.warning(
        f"BOOK DELETED | user_id={current_user.id} | book_id={book_id}"
    )

    return
