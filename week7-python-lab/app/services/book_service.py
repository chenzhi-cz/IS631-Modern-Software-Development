from sqlalchemy.orm import Session
from app.models.book import Book, BookCreate
from collections import Counter, OrderedDict
from typing import Dict

class BookService:
    def __init__(self, db: Session):
        self.db = db

    def get_books(self):
        """Retrieve all books."""
        return self.db.query(Book).all()

    def get_book(self, book_id: int):
        """Retrieve a book by ID."""
        return self.db.query(Book).filter(Book.id == book_id).first()

    def add_book(self, book_data: BookCreate):
        """Add a new book."""
        new_book = Book(**book_data.model_dump())
        self.db.add(new_book)
        self.db.commit()
        self.db.refresh(new_book)
        return new_book

    def update_book(self, book_id: int, updated_data: BookCreate):
        """Update an existing book."""
        book = self.get_book(book_id)
        if not book:
            return None
        for key, value in updated_data.model_dump().items():
            setattr(book, key, value)
        self.db.commit()
        self.db.refresh(book)
        return book

    def delete_book(self, book_id: int):
        """Delete a book by ID."""
        book = self.get_book(book_id)
        if not book:
            return False
        self.db.delete(book)
        self.db.commit()
        return True
    
    # TODO: Activity 1 and 2, Uncomment it for Code Review and Refactor
    # def count_longest_book_titles(self):
    #     """
    #      * This code replicates the Java snippet's approach 
    #      * for counting words by scanning letters vs. whitespace.
    #      * It's intentionally verbose and has code duplication 
    #      * so students can identify code smells.
    #     """
    #     allBooks = self.db.query(Book).all()

    #     selectedBooks = []  # Leftover variable, never used
    #     charcount = 0       # Debug variable, also leftover

    #     # First pass: find the maximum word count
    #     longestTitle = 0
    #     for book in allBooks:
    #         s = book.title
    #         charcount = len(s)  # debug info
    #         print(charcount)    # debug print

    #         count = 0
    #         found = False
    #         eol = len(s) - 1

    #         for i in range(len(s)):
    #             if s[i].isalpha() and i != eol:
    #                 found = True
    #             elif (not s[i].isalpha()) and found:
    #                 count += 1
    #                 found = False
    #             elif s[i].isalpha() and i == eol:
    #                 count += 1

    #         if count > longestTitle:
    #             longestTitle = count

    #     # Second pass: how many have that longest count
    #     count1 = 0
    #     for book in allBooks:
    #         s = book.title
    #         count = 0
    #         found = False
    #         eol = len(s) - 1

    #         for i in range(len(s)):
    #             if s[i].isalpha() and i != eol:
    #                 found = True
    #             elif (not s[i].isalpha()) and found:
    #                 count += 1
    #                 found = False
    #             elif s[i].isalpha() and i == eol:
    #                 count += 1

    #         if count == longestTitle:
    #             count1 += 1

    #     return count1


    def get_most_common_words_in_titles(self, top_k: int) -> Dict[str, int]:
        """
        TODO: Activity 3, Pair Programming
        Example:
          - If there are two books: 
               "I'm a Book", "This book is great"
          - Then get_most_common_words_in_titles(2) might return:
               {"book": 2, "a": 1}
          - get_most_common_words_in_titles(3) might return:
               {"book": 2, "a": 1, "is": 1}

        :param top_k: how many words to return (0 => return empty dict).
        :return: a dictionary of at most top_k words -> count, 
                 sorted by frequency desc, then alphabetically asc.
        """

        return dict()


