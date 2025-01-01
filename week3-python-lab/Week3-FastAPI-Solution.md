# Lab: Week 3 – Python FastAPI Solution

## Solution to Activity 2

### In app/routes/books.py:
```python
    @router.put("/{book_id}", response_model=BookResponse)
    def update_book(
        book_id: int,
        updated_book: BookCreate,
        book_service: BookService = Depends(get_book_service)
    ):
        """Update a book's information."""
        updated_book_info = book_service.update_book(book_id, updated_book.model_dump())
        if not updated_book_info:
            raise HTTPException(status_code=404, detail="Book not found")
        return updated_book_info

    @router.delete("/{book_id}")
    def delete_book(book_id: int, book_service: BookService = Depends(get_book_service)):
        """Remove a book."""
        success = book_service.delete_book(book_id)
        if not success:
            raise HTTPException(status_code=404, detail="Book not found")
        return {"detail": "Book deleted successfully"}
```


### In app/services/books.py:

```python
    def update_book(self, book_id: int, updated_book: dict):
        """Update an existing book."""
        book = self.get_book(book_id)
        if not book:
            return None
        book.update(updated_book)
        return book

    def delete_book(self, book_id: int):
        """Delete a book by ID."""
        book = self.get_book(book_id)
        if not book:
            return False
        self.books.remove(book)
        return True
```