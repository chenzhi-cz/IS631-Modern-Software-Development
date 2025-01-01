### **Week 6 Software Testing**

---

#### **Preparation Work**

1. **Download the Lab Repository**:
You can use [DownGit](https://downgit.github.io/#/) to download only the specific folder you need from the repository.

- 1. **Open DownGit**  
   Visit [https://downgit.github.io/#/](https://downgit.github.io/#/).

- 2. **Paste the Folder URL**  
   Use the following URL for the `week6-python-lab` folder:
   ```
   https://github.com/chenzhi-cz/IS631-Modern-Software-Development/tree/main/week6-python-lab
   ```

- 3. **Download the Folder**  
   - Paste the URL into the DownGit interface.
   - Click the "Download" button.
   - A `.zip` file containing only the `week6-python-lab` folder will be downloaded.

- 4. **Extract the Folder**  
   Extract the `.zip` file to access the `week6-python-lab` content.


Below is **Activity 1** for a *Software Testing Lab* that guides students through writing and running tests for a FastAPI application. It covers fundamental testing concepts, introduces mocking, and provides step-by-step instructions on how to run the tests.

---

# **Activity 1: Introduction to Testing with FastAPI and Pytest**

## **Objective**

1. Familiarize yourself with basic testing concepts and best practices.
2. Understand how to use **FastAPI’s** dependency injection mechanism in tests.
3. Learn how to **mock** external dependencies (e.g., database or service calls) to isolate and test individual components.
4. Successfully run the tests locally using `pytest`.

---

## **Part 1: Basic Concepts of Software Testing**

1. **Unit Testing**  
   - **Definition**: Testing individual components or functions in isolation.  
   - **Goal**: Ensure each function behaves correctly under various conditions.

2. **Integration Testing**  
   - **Definition**: Testing how multiple components interact with each other.  
   - **Goal**: Confirm that the system works correctly when modules are combined.

3. **End-to-End (E2E) Testing**  
   - **Definition**: Testing the entire workflow from start to finish, simulating real user scenarios.  
   - **Goal**: Verify that the entire application stack works together and meets requirements.

In this lab activity, we’ll focus primarily on **unit and integration tests** for the routes in our FastAPI application.

---

## **Part 2: Why We Use Mocks**

- **Definition**: A **mock** is a fake or in-memory replacement for a real dependency.
- **Purpose**:  
  1. *Isolation*: We can test our route logic without relying on a real database or external services.  
  2. *Speed*: Tests run faster because they don’t do real I/O or network calls.  
  3. *Reliability*: Tests don’t fail due to external systems being down or slow.  

When we “mock” a service, we replace its methods (e.g., `add_book`, `get_books`) with test doubles. We can then track how many times they were called and with which arguments.

---

## **Part 3: Example Test File Structure**

Assume we have the following files:

- **`app/routes/books.py`** (the FastAPI routes)
- **`app/services/book_service.py`** (the actual service logic)
- **`app/models/book.py`** (Pydantic models)
- **`tests/test_books_routes.py`** (our test file)

A simplified `test_books_routes.py` might look like this:

```python
import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient

from app.main import app
from app.models.book import BookCreate, BookResponse
from app.services.book_service import BookService
from app.routes.books import get_book_service

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def mock_book_service():
    # We create a mock for the BookService
    return MagicMock(spec=BookService)

@pytest.fixture
def override_book_service(mock_book_service):
    # This overrides our get_book_service dependency
    app.dependency_overrides[get_book_service] = lambda: mock_book_service
    yield
    app.dependency_overrides = {}

def test_add_book(client, mock_book_service, override_book_service):
    mock_book_service.add_book.return_value = BookResponse(
        id=1,
        title="New Book",
        author="Author1",
        year=2023,
        description="Test Description"
    )

    payload = {
        "title": "New Book",
        "author": "Author1",
        "year": 2023,
        "description": "Test Description",
    }

    response = client.post("/books/", json=payload)

    # Assertions
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "title": "New Book",
        "author": "Author1",
        "year": 2023,
        "description": "Test Description"
    }
    # Verify our mock method was called
    from app.models.book import BookCreate
    mock_book_service.add_book.assert_called_once_with(BookCreate(**payload))
```

### Explanation

1. We **override** the `get_book_service` dependency so that every route that depends on it will receive our `mock_book_service` instead of a real one.
2. **`mock_book_service.add_book.return_value`** is set to a fake `BookResponse`, simulating a successful “add book” operation.
3. We make a **POST** request to the `/books/` endpoint via `client.post(...)`.
4. We check:  
   - The status code is **200** (success).  
   - The response body matches the mocked return value.  
   - `mock_book_service.add_book` was called exactly once with the correct `BookCreate` object.

---

## **Part 4: Running the Tests**

1. **Install Dependencies**  
   Make sure you have a virtual environment set up and that you’ve installed all necessary packages in requirements.txt
   (Adjust according to your project .)

2. **Navigate to Your Project Folder**  
   ```bash
   cd path/to/your/project
   ```

3. **Run Pytest**  
   ```bash
   pytest
   ```
   Pytest will discover all files that match the pattern `test_*.py` or `*_test.py` and run them automatically.

4. **View Test Results**  
   You should see output indicating which tests passed or failed. Example:
   ```txt
   ================= test session starts =================
   collected 8 items

   tests/test_books_routes.py ........                  [100%]

   ================= 8 passed in 0.12s ==================
   ```

5. **Debugging Failures**  
   If any test fails, read the error message to identify the cause. Common errors include:  
   - *Dependency not overridden correctly.*  
   - *Mock methods not called with the expected arguments.*  
   - *Mismatched JSON response.*  
   - *Typos in endpoint URLs.*

---


# **Activity 2: Mocking the Database and Testing Review APIs**

## **Objective**

1. **Reinforce** understanding of how to **mock** a database session in unit tests so that you **don’t need** a real database connection.
2. **Read and analyze** the existing test code for `BookService` (`test_book_service.py`) to understand how queries, commits, and rollbacks are handled in tests with a mocked DB.
3. **Write and run** tests for the **Reviews** functionality using similar mocking strategies learned from `BookService`.

---

## **Part 1: Review the Existing `test_book_service.py`**

1. **Open** the `test_book_service.py` file (or the equivalent you have from Activity 1).
2. **Observe** how the `Session` object is replaced with a `MagicMock(spec=Session)`.  
   - `mock_db_session.query.return_value.all.return_value = [...]`  
   - `mock_db_session.query.return_value.filter.return_value.first.return_value = some_book`
3. **Note** the usage of methods like `mock_db_session.add(...)`, `mock_db_session.commit(...)`, and `mock_db_session.refresh(...)`, and how they are **asserted** or **configured** with side effects (e.g., setting an ID on a newly created book).

### **Why Do We Mock the DB?**
- **No Real DB Needed**: We don’t have to configure or spin up a local or remote database to run our tests.  
- **Isolation**: This keeps our tests focused on **service logic** rather than external factors.  
- **Speed**: It’s typically much faster to run tests that don’t touch a real database.

---

## **Part 2: Apply These Concepts to `ReviewService`**

The steps to test it with a mocked DB session are almost identical:

1. **Create a test file** (e.g., `test_review_service.py`).
2. **Use** the same approach as in `test_book_service.py`:
   - Import `ReviewService`, your `Review` or `ReviewCreate` models, and **pytest** or **unittest.mock** as needed.
   - Create a `mock_db_session` fixture using `MagicMock(spec=Session)`.
   - Write tests that:
     - Set up the **return values** for `.query(...)`, `.filter(...)`, or `.all()`.
     - Verify that the correct queries and DB operations (`add`, `commit`, `refresh`, `delete`) are made.
     - Check the expected return data (or `None/False` if something isn’t found).


## **Part 3: Testing the Review Routes (Optional Extension)**

You can also create a `test_reviews_routes.py`:

1. **Override** the `get_review_service` dependency (similar to how you did with `get_book_service`).  
2. **Mock** the methods of `ReviewService` so the route can be tested without a real DB.  
3. **Use** `client = TestClient(app)` to call the endpoints directly in your tests.

## **Part 4: Student Tasks**

1. **Read the Code**  
   - Carefully examine `test_book_service.py` to see how the `Session` is mocked.  
   - Note how queries and DB operations are configured to return different data.

2. **Build Tests for `ReviewService`**  
   - Create `test_review_service.py`.  
   - Use `mock_db_session` to simulate DB responses:
     - **Found** vs **Not Found** scenarios.  
     - Handling **valid** vs **invalid** data (e.g., rating out of range, empty content, etc.).
   - Use `assert` statements to verify correct logic (e.g., check the returned review’s fields, confirm the DB operations are called).

3. **(Optional) Test the Review Routes**  
   - Create `test_reviews_routes.py` (or similar).  
   - Override the `get_review_service` dependency.  
   - Mock the service methods.  
   - Make actual **HTTP** requests to the review endpoints using `TestClient`.

4. **Run All Tests**  
   - Ensure all your tests pass:
     ```bash
     pytest
     ```
   - Fix any **assertion errors** or **validation errors** that appear.



# **Activity 3: Testing Coverage**

---

## 1. Install `pytest-cov`

```bash
pip install pytest-cov
```

This installs the pytest plugin that will gather code coverage metrics as your tests run.

---

## 2. Create a `.coveragerc` File (Optional, but Recommended)

Use a `.coveragerc` file to configure coverage behavior—specifically, to **exclude** your tests directory and any other files you don’t want measured.

Create a file named **`.coveragerc`** with the following content:

```ini
[run]
# Omit the tests/ directory (adjust the path if yours is different)
omit =
    tests/*

[report]
# Example: exclude lines that contain if __name__ == '__main__':
exclude_lines =
    if __name__ == "__main__"
```

This tells coverage (via `pytest-cov`) to **omit** any files in the `tests/` directory, so you only measure coverage on your application code.

---

## 3. Run Tests with Coverage

Run your tests from the command line, specifying the `--cov` option (pointing to the **source** directory you want to measure). For example, if your application code resides in `app/`:

```bash
pytest --cov=app --cov-config=.coveragerc --cov-report=term-missing
```

- `--cov=app`: Tells `pytest-cov` to measure coverage in the `app/` folder.
- `--cov-config=.coveragerc`: Uses the settings from your `.coveragerc`.
- `--cov-report=term-missing`: Prints the coverage report in the terminal, showing lines missed.

You’ll see an output similar to:

```
---------- coverage: ... ----------
Name                Stmts   Miss  Cover   Missing
-------------------------------------------------
app/main.py            20      2    90%   12-13
app/services.py        50     10    80%   45-49, 60-64
...
-------------------------------------------------
TOTAL                  70     12    82%
```

---

## 4. Interpreting the Coverage Report

- **Coverage %**: The percentage of code lines executed by your tests.
- **Missing lines**: Specifically flagged lines or branches that your tests didn’t run.
- **Focus**: If you see lines missing coverage in critical logic, consider adding or expanding your tests to cover those scenarios.
- **Note**: High coverage doesn’t guarantee *complete correctness*—it just means lines of code have been executed. Always ensure you have meaningful assertions for each scenario.
