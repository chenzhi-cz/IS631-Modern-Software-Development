class BookService:
    def __init__(self):
        # Initialize in-memory storage for books with three preloaded books
        self.books = [
            {
                "id": 1,
                "title": "FastAPI Essentials",
                "author": "John Doe",
                "year": 2023,
                "description": "A beginner's guide to FastAPI."
            },
            {
                "id": 2,
                "title": "Advanced FastAPI",
                "author": "Jane Smith",
                "year": 2024,
                "description": "A deep dive into FastAPI's advanced features."
            },
            {
                "id": 3,
                "title": "Python for Web Development",
                "author": "Alice Brown",
                "year": 2022,
                "description": "Learn Python for building modern web applications."
            }
        ]
        self.next_id = 4  # Start ID for the next book

    def get_books(self):
        """Retrieve all books."""
        return self.books

    def get_book(self, book_id: int):
        """Retrieve a book by ID."""
        return next((book for book in self.books if book["id"] == book_id), None)

    def add_book(self, new_book: dict):
        """Add a new book."""
        new_book["id"] = self.next_id
        self.next_id += 1
        self.books.append(new_book)
        return new_book

    # def update_book(self, book_id: int, updated_book: dict):
    #     """
    #     TODO: Activity 2
    #     Add code to update an existing book.
    #     """
    #     # Your code here
    #     return None

    # def delete_book(self, book_id: int):
    #     """
    #     TODO: Activity 2
    #     Add code to remove a book with the given id
    #     """
    #     # Your code here

