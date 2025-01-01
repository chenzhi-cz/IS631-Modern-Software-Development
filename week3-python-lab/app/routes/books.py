
from fastapi import APIRouter, HTTPException, Depends
from app.models.book import BookCreate, BookResponse
from app.services.book_service import BookService

router = APIRouter()

book_service_instance = BookService()

def get_book_service() -> BookService:
    """Dependency to provide a singleton instance of BookService."""
    return book_service_instance

@router.get("/", response_model=list[BookResponse])
def get_books(book_service: BookService = Depends(get_book_service)):
    """Retrieve all books."""
    return book_service.get_books()

@router.get("/{book_id}", response_model=BookResponse)
def get_book(book_id: int, book_service: BookService = Depends(get_book_service)):
    """Retrieve a book by its ID."""
    book = book_service.get_book(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.post("/", response_model=BookResponse)
def add_book(book: BookCreate, book_service: BookService = Depends(get_book_service)):
    """Add a new book."""
    return book_service.add_book(book.model_dump())

# @router.put("/{book_id}", response_model=BookResponse)
# def update_book(
#     book_id: int,
#     updated_book: BookCreate,
#     book_service: BookService = Depends(get_book_service)
# ):
#     """
#     TODO: Activity 2
#     Add code to implement the PUT request to update book's info.
#     If there is no book with the given "id", raise an HTTPException with status 404.
    
#     :param id: Book ID
#     :param updated_book: New information to update the book
#     :return: The updated book
#     """
#     # Your code here

# @router.delete("/{book_id}")
# def delete_book(book_id: int, book_service: BookService = Depends(get_book_service)):
#     """
#     TODO: Activity 2
#     Remove a book with the DELETE request to "/books/{id}".
#     If there is no book with the given "id", raise an HTTPException with status 404.
    
#     :param id: Book ID
#     """
#     # Your code here




