# tests/test_book_service.py

import pytest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session

from app.services.book_service import BookService
from app.models.book import Book, BookCreate

@pytest.fixture
def mock_db_session():
    """
    Create a MagicMock that follows the spec of an SQLAlchemy Session.
    This ensures we have 'query', 'add', 'commit', etc.
    """
    return MagicMock(spec=Session)

def test_get_books_returns_list(mock_db_session):
    # 1) Arrange
    # Mock the query so that calling .all() returns a list of Book objects
    mock_db_session.query.return_value.all.return_value = [
        Book(id=1, title="Title1", author="Author1", year=2021, description="Desc1"),
        Book(id=2, title="Title2", author="Author2", year=2022, description="Desc2"),
    ]

    service = BookService(mock_db_session)

    # 2) Act
    books = service.get_books()

    # 3) Assert
    assert len(books) == 2
    assert books[0].title == "Title1"
    assert books[1].title == "Title2"
    # Ensure the correct calls were made
    mock_db_session.query.assert_called_once_with(Book)
    mock_db_session.query.return_value.all.assert_called_once()

def test_get_book_found(mock_db_session):
    # 1) Arrange
    mock_book = Book(id=10, title="Some Book", author="Some Author", year=2020, description="Desc")
    # Setup so that .first() returns 'mock_book'
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_book

    service = BookService(mock_db_session)

    # 2) Act
    result = service.get_book(10)

    # 3) Assert
    assert result == mock_book
    mock_db_session.query.return_value.filter.assert_called_once()
    mock_db_session.query.return_value.filter.return_value.first.assert_called_once()

def test_get_book_not_found(mock_db_session):
    # 1) Arrange
    # Setup so that .first() returns None
    mock_db_session.query.return_value.filter.return_value.first.return_value = None

    service = BookService(mock_db_session)

    # 2) Act
    result = service.get_book(999)

    # 3) Assert
    assert result is None
    mock_db_session.query.return_value.filter.assert_called_once()

def test_add_book(mock_db_session):
    # 1) Arrange
    # A new BookCreate payload
    book_data = BookCreate(
        title="New Book",
        author="New Author",
        year=2023,
        description="Testing book creation"
    )
    # We also decide what the newly-created Book object should look like
    mock_new_book = Book(
        id=1,
        title=book_data.title,
        author=book_data.author,
        year=book_data.year,
        description=book_data.description
    )

    # For .commit() and .refresh() to work, we can just mock them as no-ops
    # We'll configure .refresh() to set the new_book's id
    def refresh_side_effect(obj):
        obj.id = 1

    mock_db_session.refresh.side_effect = refresh_side_effect

    service = BookService(mock_db_session)

    # 2) Act
    result = service.add_book(book_data)

    # 3) Assert
    # Check the returned object has an ID now
    assert result.id == 1
    assert result.title == "New Book"
    # Ensure that we added, committed, and refreshed the book
    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()
    mock_db_session.refresh.assert_called_once_with(result)

def test_update_book_found(mock_db_session):
    # 1) Arrange
    existing_book = Book(
        id=10,
        title="Old Title",
        author="Old Author",
        year=2000,
        description="Old Description",
    )
    mock_db_session.query.return_value.filter.return_value.first.return_value = existing_book

    updated_data = BookCreate(
        title="New Title",
        author="New Author",
        year=2023,
        description="New Description"  # 15 characters here
    )

    service = BookService(mock_db_session)

    # 2) Act
    updated_book = service.update_book(10, updated_data)

    # 3) Assert
    assert updated_book is existing_book
    assert updated_book.title == "New Title"
    assert updated_book.year == 2023
    assert updated_book.description == "New Description"
    mock_db_session.query.return_value.filter.assert_called_once()
    mock_db_session.commit.assert_called_once()
    mock_db_session.refresh.assert_called_once_with(existing_book)

def test_update_book_not_found(mock_db_session):
    # 1) Arrange
    mock_db_session.query.return_value.filter.return_value.first.return_value = None

    service = BookService(mock_db_session)

    # 2) Act
    updated_book = service.update_book(
        999,
        BookCreate(
            title="Anything",
            author="Anyone",
            year=2020,
            description="Some text here"  # 14 characters
        )
    )

    # 3) Assert
    assert updated_book is None
    mock_db_session.commit.assert_not_called()

def test_delete_book_found(mock_db_session):
    # 1) Arrange
    existing_book = Book(id=10, title="Delete Me", author="Author", year=2000, description="Desc")
    mock_db_session.query.return_value.filter.return_value.first.return_value = existing_book

    service = BookService(mock_db_session)

    # 2) Act
    result = service.delete_book(10)

    # 3) Assert
    assert result is True
    mock_db_session.delete.assert_called_once_with(existing_book)
    mock_db_session.commit.assert_called_once()

def test_delete_book_not_found(mock_db_session):
    # 1) Arrange
    # No book found
    mock_db_session.query.return_value.filter.return_value.first.return_value = None

    service = BookService(mock_db_session)

    # 2) Act
    result = service.delete_book(999)

    # 3) Assert
    assert result is False
    mock_db_session.delete.assert_not_called()
    mock_db_session.commit.assert_not_called()

# TODO Uncomment it for Activity 1 and 2 Code Review and Refactor

# def test_count_longest_titles_one_longest_return1(mock_db_session):
#     existing_books = [
#         Book(title="The Longest"),
#         Book(title="The Longest Title"),
#         Book(title="The Longest Title of Book"),
#     ]
#     mock_db_session.query.return_value.all.return_value = existing_books
#     # Create our service and attach the mock repository
#     service = BookService(mock_db_session)

#     # 2) Act
#     count = service.count_longest_book_titles()

#     # 3) Assert
#     mock_db_session.query.assert_called_once_with(Book)
#     mock_db_session.query.return_value.all.assert_called_once()
#     assert count == 1

# def test_count_longest_titles_two_longest_return2(mock_db_session):
#     # 1) Arrange
#     existing_books = [
#         Book(title="The Longest"),
#         Book(title="The Longer Title of Book"),
#         Book(title="The Longest"),
#         Book(title="The Longest Title of Book"),
#     ]
#     mock_db_session.query.return_value.all.return_value = existing_books
#     service = BookService(mock_db_session)

#     # 2) Act
#     count = service.count_longest_book_titles()

#     # 3) Assert
#     assert count == 2
#     mock_db_session.query.assert_called_once_with(Book)
#     mock_db_session.query.return_value.all.assert_called_once()

# def test_count_longest_titles_two_longest_return4(mock_db_session):
#     # 1) Arrange
#     existing_book = [
#         Book(title="The Long Book"),
#         Book(title="The Longer Book"),
#         Book(title="The Longerer Book"),
#         Book(title="The Longest Book"),
#     ]
#     mock_db_session.query.return_value.all.return_value = existing_book
#     service = BookService(mock_db_session)

#     # 2) Act
#     count = service.count_longest_book_titles()

#     # 3) Assert
#     assert count == 4
#     mock_db_session.query.assert_called_once_with(Book)
#     mock_db_session.query.return_value.all.assert_called_once()


# TODO Uncomment it for Activity 3 Pair Programming

# def test_get_most_common_words_in_titles_return_empty_map(mock_db_session):
#     """
#     If we pass in top_k=0, we expect an empty dictionary returned.
#     This replicates @Test getMostCommonWordsInTitles_ReturnEmptyMap() in Java.
#     """
#     # 1) Arrange
#     # Mock that .all() returns any list of books, 
#     # but top_k=0 => empty dict anyway
#     mock_db_session.query.return_value.all.return_value = [
#         Book(title="Some Book"),
#         Book(title="Another Title")
#     ]
#     service = BookService(mock_db_session)

#     # 2) Act
#     actual = service.get_most_common_words_in_titles(0)

#     # 3) Assert
#     expected = {}
#     assert actual == expected

# def test_get_most_common_words_in_titles_sort_by_word_count(mock_db_session):
#     """
#     This replicates @Test getMostCommonWordsInTitles_SortByWordCount() in Java.
#     We want to confirm that words are sorted by frequency desc, 
#     and ties are sorted alphabetically.
#     """
#     # 1) Arrange
#     mock_db_session.query.return_value.all.return_value = [
#         Book(title="Book book book"),
#         Book(title="Title title"),
#         Book(title="Word word word word")
#     ]
#     service = BookService(mock_db_session)

#     # 2) Act
#     actual = service.get_most_common_words_in_titles(2)

#     # 3) Assert
#     # In these titles:
#     #  - "book" appears 3 times
#     #  - "word" appears 4 times
#     #  - "title" appears 2 times
#     # The top-2 by frequency: word(4), book(3)
#     # Return them in a dict: {"word": 4, "book": 3}
#     # Then check that the code returns exactly that.
#     expected = {"word": 4, "book": 3}
#     assert actual == expected

#     # Optionally verify the mock call
#     mock_db_session.query.assert_called_once()
