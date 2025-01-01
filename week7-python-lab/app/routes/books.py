from fastapi import APIRouter, HTTPException, Depends, Path
from sqlalchemy.orm import Session

from app.models.book import Book, BookCreate, BookResponse
from app.services.book_service import BookService
from app.db.db import SessionLocal

router = APIRouter()

# 1) Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 2) Dependency to get a BookService instance
def get_book_service(db: Session = Depends(get_db)) -> BookService:
    return BookService(db)

@router.get("/", response_model=list[BookResponse])
def get_books(service: BookService = Depends(get_book_service)):
    return service.get_books()

@router.get("/{book_id}", response_model=BookResponse)
def get_book(book_id: int, service: BookService = Depends(get_book_service)):
    book = service.get_book(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.post("/", response_model=BookResponse)
def add_book(book: BookCreate, service: BookService = Depends(get_book_service)):
    return service.add_book(book)

@router.put("/{book_id}", response_model=BookResponse)
def update_book(book_id: int, updated_book: BookCreate, service: BookService = Depends(get_book_service)):
    book = service.update_book(book_id, updated_book)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.delete("/{book_id}")
def delete_book(book_id: int, service: BookService = Depends(get_book_service)):
    success = service.delete_book(book_id)
    if not success:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": "Book deleted successfully"}
