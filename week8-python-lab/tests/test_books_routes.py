import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient

from app.main import app
from app.models.book import BookCreate, BookResponse
from app.services.book_service import BookService
from app.routes.books import get_book_service

@pytest.fixture
def client():
    """Fixture to create a new TestClient for each test."""
    return TestClient(app)

@pytest.fixture
def mock_book_service():
    """
    Create a mock for BookService that we can configure in each test.
    The `spec=BookService` argument ensures our mock has the same attributes.
    """
    return MagicMock(spec=BookService)

@pytest.fixture
def override_book_service(mock_book_service):
    """
    Override the get_book_service dependency with our mock_book_service.
    After the test ends, clear overrides.
    """
    app.dependency_overrides[get_book_service] = lambda: mock_book_service
    yield
    app.dependency_overrides = {}

def test_get_books(client, mock_book_service, override_book_service):
    """Test GET /books/ returns list of books."""
    # 1) Configure the mock's return value
    mock_book_service.get_books.return_value = [
        BookResponse(
            id=1, 
            title="Book One", 
            author="Author One", 
            year=2021,
            description="First book"
        ),
        BookResponse(
            id=2, 
            title="Book Two", 
            author="Author Two", 
            year=2022,
            description="Second book"
        ),
    ]

    # 2) Make the request
    response = client.get("/books/")

    # 3) Check the response
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "title": "Book One",
            "author": "Author One",
            "year": 2021,
            "description": "First book"
        },
        {
            "id": 2,
            "title": "Book Two",
            "author": "Author Two",
            "year": 2022,
            "description": "Second book"
        },
    ]
    mock_book_service.get_books.assert_called_once()

def test_get_book_found(client, mock_book_service, override_book_service):
    """Test GET /books/{book_id} when book is found."""
    mock_book_service.get_book.return_value = BookResponse(
        id=10,
        title="Some Book",
        author="Some Author",
        year=2020,
        description="A description"
    )

    response = client.get("/books/10")
    assert response.status_code == 200
    assert response.json() == {
        "id": 10,
        "title": "Some Book",
        "author": "Some Author",
        "year": 2020,
        "description": "A description"
    }
    mock_book_service.get_book.assert_called_once_with(10)

def test_get_book_not_found(client, mock_book_service, override_book_service):
    """Test GET /books/{book_id} returns 404 when not found."""
    mock_book_service.get_book.return_value = None  # simulate not found

    response = client.get("/books/9999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Book not found"}
    mock_book_service.get_book.assert_called_once_with(9999)

def test_add_book(client, mock_book_service, override_book_service):
    """Test POST /books/ adds a new book."""
    mock_book_service.add_book.return_value = BookResponse(
        id=123,
        title="New Book",
        author="New Author",
        year=2023,
        description="A new test book"
    )

    payload = {
        "title": "New Book",
        "author": "New Author",
        "year": 2023,
        "description": "A new test book"
    }
    response = client.post("/books/", json=payload)
    assert response.status_code == 200
    assert response.json() == {
        "id": 123,
        "title": "New Book",
        "author": "New Author",
        "year": 2023,
        "description": "A new test book"
    }

    # Verify the mock was called with a BookCreate object that has the same data
    from app.models.book import BookCreate  # local import to avoid circular
    mock_book_service.add_book.assert_called_once_with(BookCreate(**payload))

def test_update_book_found(client, mock_book_service, override_book_service):
    """Test PUT /books/{book_id} successfully updates a book."""
    mock_book_service.update_book.return_value = BookResponse(
        id=10,
        title="Updated Book",
        author="Updated Author",
        year=2025,
        description="An updated description"
    )

    payload = {
        "title": "Updated Book",
        "author": "Updated Author",
        "year": 2025,
        "description": "An updated description"
    }
    response = client.put("/books/10", json=payload)
    assert response.status_code == 200
    assert response.json() == {
        "id": 10,
        "title": "Updated Book",
        "author": "Updated Author",
        "year": 2025,
        "description": "An updated description"
    }

    from app.models.book import BookCreate
    mock_book_service.update_book.assert_called_once_with(10, BookCreate(**payload))

def test_update_book_not_found(client, mock_book_service, override_book_service):
    """Test PUT /books/{book_id} returns 404 if the book is not found."""
    mock_book_service.update_book.return_value = None  # simulate not found

    payload = {
        "title": "Nonexistent Book",
        "author": "No Author",
        "year": 1900,
        "description": "No description"
    }
    response = client.put("/books/9999", json=payload)
    assert response.status_code == 404
    assert response.json() == {"detail": "Book not found"}
    from app.models.book import BookCreate
    mock_book_service.update_book.assert_called_once_with(9999, BookCreate(**payload))

def test_delete_book_found(client, mock_book_service, override_book_service):
    """Test DELETE /books/{book_id} returns success if the book was deleted."""
    mock_book_service.delete_book.return_value = True  # book found & deleted

    response = client.delete("/books/10")
    assert response.status_code == 200
    assert response.json() == {"message": "Book deleted successfully"}
    mock_book_service.delete_book.assert_called_once_with(10)

def test_delete_book_not_found(client, mock_book_service, override_book_service):
    """Test DELETE /books/{book_id} returns 404 if the book doesn't exist."""
    mock_book_service.delete_book.return_value = False  # simulate not found

    response = client.delete("/books/9999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Book not found"}
    mock_book_service.delete_book.assert_called_once_with(9999)
