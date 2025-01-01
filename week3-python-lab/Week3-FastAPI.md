# Lab: Week 3 – Modern Software Solution Development with Python FastAPI 

## Introduction

This lab guides you through developing a RESTful API using Python's **FastAPI** framework. You will learn how to implement CRUD operations, integrate the OpenAI API for text generation, and document your API using Swagger UI.

## Before Class – Setup (Individual)

1. **Install Prerequisites**:
   - Install **Python 3.10+** from [Python.org](https://www.python.org/).
   - Install **Visual Studio Code** or another IDE for Python development.
   - Install the following extensions in VS Code (Ctrl+Shift+X):
     - Pylance by Microsoft
     - REST Client by Huachao Mao.

2. **Download the Lab Repository**:
You can use [DownGit](https://downgit.github.io/#/) to download only the specific folder you need from the repository.

- 1. **Open DownGit**  
   Visit [https://downgit.github.io/#/](https://downgit.github.io/#/).

- 2. **Paste the Folder URL**  
   Use the following URL for the `week3-python-lab` folder:
   ```
   https://github.com/chenzhi-cz/IS631-Modern-Software-Development/tree/main/week3-python-lab
   ```

- 3. **Download the Folder**  
   - Paste the URL into the DownGit interface.
   - Click the "Download" button.
   - A `.zip` file containing only the `week3-python-lab` folder will be downloaded.

- 4. **Extract the Folder**  
   Extract the `.zip` file to access the `week3-python-lab` content.

3. **Set Up a Virtual Environment**:
   Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows, use venv\Scripts\activate
   ```

4. **Install Dependencies**:
   Install project dependencies using the `requirements.txt` file:
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the Application**:
   Start the FastAPI application:
   ```bash
   uvicorn app.main:app --reload
   ```

6. **Access the API**:
   - API Endpoints: `http://localhost:8000`
   - Swagger Documentation: `http://localhost:8000/docs`

---

## Activity 1: Dependency Injection with FastAPI

### Objective:
Learn about dependency injection (DI) and how services are used in FastAPI to create modular, testable, and maintainable code.

### What is Dependency Injection?
Dependency Injection is a design pattern where objects (dependencies) are provided to a class or function rather than being created inside it. This allows for:
- **Modularity**: Different parts of the application can be developed and tested independently.
- **Flexibility**: Dependencies can be replaced with alternatives (e.g., mocks) during testing or configuration changes.
- **Reusability**: The same dependency (e.g., a service) can be reused across multiple parts of the application.

In FastAPI, DI is implemented using the `Depends` function. `Depends` acts as a marker to declare that a particular route or function relies on an external dependency. FastAPI handles the lifecycle and injection of these dependencies automatically.

### How Does `Depends` Work in FastAPI?
FastAPI uses the `Depends` function to:
1. Indicate a dependency (e.g., a service class like `BookService`) that should be injected into a route or function.
2. Automatically resolve the dependency by calling the specified provider function and passing the result to the route or function.

For example, instead of creating a `BookService` instance in every route, you define a dependency provider (a function) that creates and manages the `BookService` instance. The route can then use `Depends` to receive this instance whenever needed.

---

### Tasks:

1. **Understand the Service**:
   - Open the `services/book_service.py` file.
   - Review the `BookService` class, which provides methods to manage book data (e.g., retrieving, adding, updating, and deleting books).

2. **Examine Dependency Injection in Action**:
   - Open the `routes/books.py` file.
   - Notice how the `BookService` instance is injected into route functions using FastAPI's `Depends` function.
   - Look at the `get_book_service` function. This is a **provider function** that FastAPI uses to supply a `BookService` instance wherever `Depends(get_book_service)` is used.

---

### Example:

Consider this code snippet from `routes/books.py`:

```python
book_service_instance = BookService()

def get_book_service() -> BookService:
    """Dependency to provide a singleton instance of BookService."""
    return book_service_instance

@router.get("/", response_model=list[BookResponse])
def get_books(book_service: BookService = Depends(get_book_service)):
    """Retrieve all books."""
    return book_service.get_books()
```

- **Provider Function**: `get_book_service` is a function that creates and returns a `BookService` instance. It acts as the dependency provider.
- **Dependency Injection**: The `Depends(get_book_service)` ensures that FastAPI will:
  1. Call `get_book_service` to create the `BookService` instance.
  2. Inject the result (`book_service`) into the `get_books` route.

---

### Benefits of Using `Depends`:
- **Testability**: You can mock `get_book_service` during testing to simulate various behaviors without relying on the real implementation.
- **Scalability**: Dependency injection allows you to easily modify the `BookService` (e.g., adding caching or database integration) without changing the route code.
- **Clarity**: The code clearly shows what dependencies each route relies on, making it easier to maintain and extend.

---

### Activity Checkpoints:
- **Step 1**: Understand the role of the `BookService` class in managing book data.
- **Step 2**: Explore how `Depends(get_book_service)` is used in `routes/books.py` to inject the `BookService`.
- **Step 3**: Reflect on how this design improves code organization and testability.

---

## Activity 2: Developing a Web Service with FastAPI

### Objective:
Create RESTful APIs for CRUD operations on books.

### Tasks:
1. Open `routes/books.py` to explore the REST API endpoints:
   - **GET /books**: Retrieve all books.
   - **GET /books/{id}**: Retrieve a book by its ID.
   - **POST /books**: Add a new book.

2. Test these endpoints using Swagger UI (`http://localhost:8000/docs`) or the REST Client.

3. **Task for Students**:
   - Implement the PUT and DELETE requests. Look for the TODO comments in  `routes/books.py`, and `services/book_service.py`.java. Test the changes using REST client

---

## Activity 3: Consuming a Web Service

### Objective:
Interact with the REST API using external tools like Swagger UI, Postman, or REST Client.

### Tasks:
1. Use the provided `client.py` file to test the CRUD endpoints. Run it with `python client.py`
2. **Task for Students**:
   - You can write additional REST requests to test other apis.

---

## Activity 4: OpenAI Integration – "Introduce a Book to Me"

### Objective:
Integrate OpenAI's text generation capabilities to create book introductions.

### Tasks:
1. **Explore the `/ai/introduce/{book_id}` Endpoint**:
   - This API fetches a book's details and generates an introduction using OpenAI's API.
   - Example Request:
     ```http
     GET http://localhost:8000/ai/introduce/1
     ```
   - Example Response:
     ```json
      {
      "book_id": 1,
      "introduction": "\"FastAPI Essentials\" is a comprehensive guide for beginners to learn about FastAPI, a high-performance Python web framework. Written by renowned author John Doe, this book takes a hands-on approach to teaching readers how to build web applications quickly and efficiently using FastAPI. \n\nStarting with the basics, readers will gain a solid understanding of the key concepts, features, and tools of FastAPI. They will learn how to set up a development environment, handle HTTP requests, and create data models. Readers will also discover how to work with databases, add authentication and authorization to their applications, and deploy their projects to the cloud.\n\nWhat sets \"FastAPI Essentials\" apart is its practical approach to teaching. Each chapter is filled with real-life examples and step"
      }
     ```

2. **Test the Endpoint**:
   - Call the `/ai/introduce/{book_id}` API with different book IDs and observe the generated text.
   - Ensure OpenAI API integration is configured with your API key in the `.env` file:
     ```
     OPENAI_API_KEY=your_openai_api_key
     ```

3. **Task for Students**:
   - Experiment with modifying the OpenAI prompt or parameters (e.g., `max_tokens`, `temperature`) in the code and observe the results.

---

## Activity 5: API Documentation with Swagger UI

### Objective:
Explore the auto-generated API documentation provided by FastAPI.

### Tasks:
1. Access the Swagger UI documentation at `http://localhost:8000/docs`.
2. Review all endpoints, including `/books` (CRUD) and `/ai/introduce`.
3. **Task for Students**:
   - Add descriptions to the endpoints in the route files (`routes/books.py` and `routes/ai.py`) for better documentation.
   - Verify the changes appear in the Swagger UI.

---
