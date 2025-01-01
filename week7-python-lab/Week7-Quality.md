# **Week 7 Lab: Code Review – Refactoring – Pair Programming (Python Version)**

#### **Preparation Work**

1. **Download the Lab Repository**:
You can use [DownGit](https://downgit.github.io/#/) to download only the specific folder you need from the repository.

- 1. **Open DownGit**  
   Visit [https://downgit.github.io/#/](https://downgit.github.io/#/).

- 2. **Paste the Folder URL**  
   Use the following URL for the `week7-python-lab` folder:
   ```
   https://github.com/chenzhi-cz/IS631-Modern-Software-Development/tree/main/week7-python-lab
   ```

- 3. **Download the Folder**  
   - Paste the URL into the DownGit interface.
   - Click the "Download" button.
   - A `.zip` file containing only the `week7-python-lab` folder will be downloaded.

- 4. **Extract the Folder**  
   Extract the `.zip` file to access the `week7-python-lab` content.

## **Activity 1: Code Review**

### **(a) Unrefined Implementation of `count_longest_book_titles`**

> **Task**: Add (or copy) this method into your **`BookService`** class (e.g., in `book_service.py`), then **review** it for code smells or potential issues.

```python
# file: app/services/book_service.py

    def count_longest_book_titles(self) -> int:
        """
        Count how many books have the 'longest' title 
        (measured by word count). This is a *two-pass* approach 
        that tries to mimic the Java snippet’s logic 
        for detecting words by scanning letters vs. whitespace.
        """
        all_books = self.books.find_all()
        
        longest_title = 0
        # First pass: find the maximum word count
        for book in all_books:
            s = book.title
            count = 0
            found = False
            eol = len(s) - 1

            for i in range(len(s)):
                if i != eol and s[i].isalpha():
                    found = True
                elif (not s[i].isalpha()) and found:
                    count += 1
                    found = False
                elif s[i].isalpha() and i == eol:
                    count += 1
            
            if count > longest_title:
                longest_title = count

        count_of_longest = 0
        # Second pass: count how many match that longest word count
        for book in all_books:
            s = book.title
            count = 0
            found = False
            eol = len(s) - 1

            for i in range(len(s)):
                if i != eol and s[i].isalpha():
                    found = True
                elif (not s[i].isalpha()) and found:
                    count += 1
                    found = False
                elif s[i].isalpha() and i == eol:
                    count += 1

            if count == longest_title:
                count_of_longest += 1

        return count_of_longest
```

### **(b) Create Tests **

```python
# file: tests/test_book_service.py


def test_count_longest_titles_one_longest_return1(mock_db_session):
    # 1) Arrange
    # Prepare a mock 'books' repository that returns a specific list of Book objects
    mock_books_repo = MagicMock()
    mock_books_repo.find_all.return_value = [
        Book(title="The Longest"),
        Book(title="The Longest Title"),
        Book(title="The Longest Title of Book"),
    ]

    # Create the service with a mock DB session
    service = BookService(mock_db_session)
    # Inject the mock 'books' repo so that `count_longest_book_titles` can use it
    service.books = mock_books_repo

    # 2) Act
    count = service.count_longest_book_titles()

    # 3) Assert
    assert count == 1
    mock_books_repo.find_all.assert_called_once()


def test_count_longest_titles_two_longest_return2(mock_db_session):
    # 1) Arrange
    mock_books_repo = MagicMock()
    mock_books_repo.find_all.return_value = [
        Book(title="The Longest"),
        Book(title="The Longer Title of Book"),
        Book(title="The Longest"),
        Book(title="The Longest Title of Book"),
    ]

    service = BookService(mock_db_session)
    service.books = mock_books_repo

    # 2) Act
    count = service.count_longest_book_titles()

    # 3) Assert
    assert count == 2
    mock_books_repo.find_all.assert_called_once()


def test_count_longest_titles_all_longest_return4(mock_db_session):
    # 1) Arrange
    mock_books_repo = MagicMock()
    mock_books_repo.find_all.return_value = [
        Book(title="The Long Book"),
        Book(title="The Longer Book"),
        Book(title="The Longerer Book"),
        Book(title="The Longest Book"),
    ]

    service = BookService(mock_db_session)
    service.books = mock_books_repo

    # 2) Act
    count = service.count_longest_book_titles()

    # 3) Assert
    assert count == 4
    mock_books_repo.find_all.assert_called_once()

```

### **(c) Run the Tests**

1. **Install** `pytest` (if needed):
   ```bash
   pip install pytest
   ```
2. **Run**:
   ```bash
   pytest
   ```

Observe which tests pass or fail, and note any particular behaviors.

### **(d) Identify Code Smells / Issues**

> **Task**: Inspect the `count_longest_book_titles` method carefully.  
> **Goal**: Create a list of **issues**, **smells**, or **improvements** needed.  

Consider:
- Does it do more than one pass over the data?  
- Is the manual scanning of letters vs. whitespace too **complex** or “un-Pythonic”?  
- Are edge cases (like empty strings or punctuation) handled well?

---

## **Activity 2: Refactoring**

### **(a) Refactor the Method**

> **Task**: Based on the issues you found, **improve** or **simplify** `count_longest_book_titles`.  
- Make it more maintainable while still passing all the tests.

---

## **Activity 3: Pair Programming**

### **(a) [Optional] Install Live Share for VS Code**

If you want to do real-time pairing, follow the [official Live Share setup guide](https://code.visualstudio.com/learn/collaboration/live-share).


## **(b) Code Setup**

You’ll open your Python project in **VS Code**, just as you did for previous labs (Week 6, etc.). Ensure you have all dependencies (pytest, a mock library, etc.) installed in your virtual environment.

---

## **BookService with `get_most_common_words_in_titles`**

You need to **implement** the following `get_most_common_words_in_titles` method.

```python
from collections import Counter, OrderedDict
from typing import Dict
from sqlalchemy.orm import Session

from app.models.book import Book  # adjust import path if needed

class BookService:
    """
    Activity 2 (Week 7) – Pair-programming exercise (Python version):
    Return the k-most common words (case insensitive) in all book titles.
    The words returned (in a dict) are sorted by:
      1) word count (descending), 
      2) then alphabetical order (ascending).
    """

    def __init__(self, db: Session):
        self.db = db

    def get_most_common_words_in_titles(self, top_k: int) -> Dict[str, int]:
        """
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
```

---

## **(b) Example Test Cases**

Here are **two** unit tests, Copy them to `test_book_service.py`. Only one of them will pass for now. You will need to write more test cases as you go along.

```python
import pytest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session

from collections import OrderedDict
from app.services.book_service import BookService
from app.models.book import Book

@pytest.fixture
def mock_db_session():
    """Provides a MagicMock for SQLAlchemy Session."""
    return MagicMock(spec=Session)

def test_get_most_common_words_in_titles_return_empty_map(mock_db_session):
    """
    If we pass in top_k=0, we expect an empty dictionary returned.
    """
    # 1) Arrange
    # Mock that .all() returns any list of books, 
    # but top_k=0 => empty dict anyway
    mock_db_session.query.return_value.all.return_value = [
        Book(title="Some Book"),
        Book(title="Another Title")
    ]
    service = BookService(mock_db_session)

    # 2) Act
    actual = service.get_most_common_words_in_titles(0)

    # 3) Assert
    expected = {}
    assert actual == expected

def test_get_most_common_words_in_titles_sort_by_word_count(mock_db_session):
    # 1) Arrange
    mock_db_session.query.return_value.all.return_value = [
        Book(title="Book book book"),
        Book(title="Title title"),
        Book(title="Word word word word")
    ]
    service = BookService(mock_db_session)

    # 2) Act
    actual = service.get_most_common_words_in_titles(2)

    # 3) Assert
    # In these titles:
    #  - "book" appears 3 times
    #  - "word" appears 4 times
    #  - "title" appears 2 times
    # The top-2 by frequency: word(4), book(3)
    # Return them in a dict: {"word": 4, "book": 3}
    # Then check that the code returns exactly that.
    expected = {"word": 4, "book": 3}
    assert actual == expected

    # Optionally verify the mock call
    mock_db_session.query.assert_called_once()
```

## **(c) Pair-Programming**

You can decide which **pairing style** to use:

- **Ping-Pong**: One partner writes a test, the other writes code to pass that test, and so on.
- **Driver-Navigator**: One partner codes (driver) while the other reviews and guides (navigator).
- **Strong-Style**: The typist only does what their pair instructs step by step.

**Goal**: Collaborate to **fully implement and test** `get_most_common_words_in_titles`. Add more test cases (e.g., checking alphabetical tie-breakers, punctuation handling, etc.).

---

## **(d) Pair-Programming Survey**

Upon completion, fill out a **pair programming** survey (like the provided Google Form link). Reflect on:

1. How the session went (challenges, successes).
2. Which pairing style you used and how you liked it.
3. Lessons learned from implementing a real-world feature as a pair.

