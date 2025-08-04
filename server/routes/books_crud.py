from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from deps import get_db
from models import Book, User, Vote
from schemas import BookResponse, BookCreate, BookUpdate, BookWithOwner, BookWithVotes
from typing import List, Optional
from oath2 import get_current_user

router = APIRouter()


@router.get("/books", response_model=List[BookWithVotes])
def get_books(
    db: Session = Depends(get_db),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
):
    # Query books with vote count
    query = (
        db.query(Book, func.count(Vote.book_id).label("votes"))
        .outerjoin(Vote, Book.id == Vote.book_id)
        .group_by(Book.id)
    )

    # Apply search filter if provided
    if search:
        query = query.filter(Book.title.contains(search))

    # Apply pagination
    results = query.offset(skip).limit(limit).all()

    # Convert to BookWithVotes objects
    books_with_votes = []
    for book, votes in results:
        book_dict = {
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "price": book.price,
            "created_at": book.created_at,
            "owner_id": book.owner_id,
            "votes": votes or 0,
            "owner": book.owner,
        }
        books_with_votes.append(BookWithVotes(**book_dict))

    return books_with_votes


@router.get("/books/{book_id}", response_model=BookWithOwner)
def get_book(book_id: int, db: Session = Depends(get_db)):
    # TODO: get the book with the votes and the owner
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.post("/books", response_model=BookResponse)
def create_book(
    book: BookCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_book = Book(owner_id=current_user.id, **book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


@router.put("/books/{book_id}", response_model=BookResponse)
def update_book(
    book_id: int,
    book: BookUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")

    # Check if user owns the book
    if db_book.owner_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to update this book"
        )

    update_data = book.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_book, key, value)

    db.commit()
    db.refresh(db_book)
    return db_book


@router.patch("/books/{book_id}", response_model=BookResponse)
def update_book_partial(
    book_id: int,
    book: BookUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")

    # Check if user owns the book
    if db_book.owner_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to update this book"
        )

    update_data = book.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_book, key, value)

    db.commit()
    db.refresh(db_book)
    return db_book


@router.delete("/books/{book_id}", status_code=204)
def delete_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    if book.owner_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to delete this book"
        )
    db.delete(book)
    db.commit()
    return None


@router.get("/users/{user_id}/books", response_model=List[BookResponse])
def get_user_books(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user.books
