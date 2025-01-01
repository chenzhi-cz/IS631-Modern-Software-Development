# Lab: Week 4 – Modern Software Solution Development with FastAPI and SQLAlchemy and ChromaDB

## Introduction

This lab guides you through developing a RESTful API using Python's FastAPI framework and integrating it with SQLAlchemy ORM for database interactions. You will also learn how to use ChromaDB, a vector database, to perform semantic searches based on text embeddings. Additionally, you will implement CRUD operations, integrate the OpenAI API for text generation, and document your API using Swagger UI.

---

## Before Class – Setup (Individual)

Read SQLAlchemy and Alembic Basics:

- SQLAlchemy: Understand Base, Session, and ORM concepts.
- Alembic: Learn how to manage database migrations.

1. **Install Prerequisites**:
   - Install the following extensions in VS Code (Ctrl+Shift+X):
     - SQLite Viewer by Florian Klampfer.

2. **Download the Lab Repository**:
You can use [DownGit](https://downgit.github.io/#/) to download only the specific folder you need from the repository.

- 1. **Open DownGit**  
   Visit [https://downgit.github.io/#/](https://downgit.github.io/#/).

- 2. **Paste the Folder URL**  
   Use the following URL for the `week4-python-lab` folder:
   ```
   https://github.com/chenzhi-cz/IS631-Modern-Software-Development/tree/main/week4-python-lab
   ```

- 3. **Download the Folder**  
   - Paste the URL into the DownGit interface.
   - Click the "Download" button.
   - A `.zip` file containing only the `week4-python-lab` folder will be downloaded.

- 4. **Extract the Folder**  
   Extract the `.zip` file to access the `week4-python-lab` content.

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

5. **Initialize the Database**

Follow these steps to set up and manage the SQLite database for your project using Alembic and SQLAlchemy.

---

 **Step 5.1: Initialize Alembic**
1. Run the following command to initialize Alembic in your project:
   ```bash
   alembic init migrations
   ```
   - This creates a `migrations` directory with the following structure:
     ```
     migrations/
       env.py
       README
       script.py.mako
       versions/
     ```
   - The `env.py` file is the main configuration file for Alembic.

---

**Step 5.2: Update the Database URL**
1. Open the `alembic.ini` file in the root of your project.
2. Update the `sqlalchemy.url` setting with the path to your SQLite database:
   ```ini
   sqlalchemy.url = sqlite:///./app.db
   ```
   - This points to an SQLite database file named `app.db` in your project root.

---

 **Step 5.3: Configure `env.py` for Model Detection**
1. Open the file `migrations/env.py`.
2. Update the file to include your `Book` and `Review` models.
3. Modify `env.py` as follows:

   ```python
   from logging.config import fileConfig
   from sqlalchemy import engine_from_config, pool
   from alembic import context

   # Import your SQLAlchemy models
   from app.db.db import Base
   from app.models.book import Book  # Import Book model
   from app.models.review import Review  # Import Review model

   # Set up Alembic Config
   config = context.config
   fileConfig(config.config_file_name)

   # Set the target metadata to Base.metadata
   target_metadata = Base.metadata

   def run_migrations_offline():
       """Run migrations in 'offline' mode."""
       context.configure(
           url=config.get_main_option("sqlalchemy.url"),
           target_metadata=target_metadata,
           literal_binds=True,
       )
       with context.begin_transaction():
           context.run_migrations()

   def run_migrations_online():
       """Run migrations in 'online' mode."""
       connectable = engine_from_config(
           config.get_section(config.config_ini_section),
           prefix="sqlalchemy.",
           poolclass=pool.NullPool,
       )

       with connectable.connect() as connection:
           context.configure(connection=connection, target_metadata=target_metadata)

           with context.begin_transaction():
               context.run_migrations()

   if context.is_offline_mode():
       run_migrations_offline()
   else:
       run_migrations_online()
   ```

   - This ensures that Alembic knows about your `Book` and `Review` models by referencing `Base.metadata`.

---

**Step 5.4: Create a Migration File**
1. Run the following command to generate a migration file based on your `Book` and `Review` models:
   ```bash
   alembic revision --autogenerate -m "Create books and reviews tables"
   ```
   - Alembic compares your `Base.metadata` (which includes `Book` and `Review` models) with the current database schema and generates the SQL commands required to create the tables.
   - The migration file will be created in the `migrations/versions` directory.

---

**Step 5.5: Apply the Migration**
1. Apply the migration to create the `books` and `reviews` tables in the database:
   ```bash
   alembic upgrade head
   ```
   - This runs the migration script and creates the database schema in `app.db`.

---

 **Step 5.6: Verify the Setup**
1. Open the SQLite database file (`app.db`) using **SQLite Viewer** in VS Code or another SQLite client.
2. Verify that the `books` and `reviews` tables are created and match the schema defined in your models.

---

**Final Commands Summary**
Run these commands sequentially:
- Initialize Alembic:
   ```bash
   alembic init migrations
   ```
- Update the database URL in `alembic.ini`:
   ```ini
   sqlalchemy.url = sqlite:///./app.db
   ```
- Create the migration:
   ```bash
   alembic revision --autogenerate -m "Create books and reviews tables"
   ```
- Apply the migration:
   ```bash
   alembic upgrade head
   ```

- Verify the Database: Open app.db using `SQLite Viewer` in VS Code, confirm the books table is created.

6. **Run the Application**:
   Start the FastAPI application:
   ```bash
   uvicorn app.main:app --reload
   ```

7. **Access the API**:
   - API Endpoints: `http://localhost:8000`
   - Swagger Documentation: `http://localhost:8000/docs`

---

### **Activity 1: Working with SQLAlchemy for CRUD Operations**
- **Objective**: Use SQLAlchemy ORM to interact with a SQLite database and implement basic CRUD (Create, Read, Update, Delete) operations for a `Book` entity.
- **Key Tasks**:
  1. Understand and review the code in `models/book.py`, `services/book_service.py`, and `routes/books.py`.
  2. Implement the following methods:
     - `updateBook` in the `BookService` class within `services/book_service.py`.
  3. Update the routes in `routes/books.py` to use the implemented methods in `BookService`.
  4. Test all endpoints using Swagger UI or the REST Client:
     - GET `/books`
     - POST `/books`
     - PUT `/books/{id}`
     - DELETE `/books/{id}`

- **Notes**:
  - Use SQLite as the database. The schema is managed via **Alembic migrations**.
  - You can view the database using **SQLite Viewer** in VS Code.

---

### **Activity 2: Modeling Relationships with SQLAlchemy**
- **Objective**: Use SQLAlchemy to manage database persistence for `Book` and `Review` entities, focusing on modeling relationships.
- **Key Tasks**:
  1. Understand the relationship between `Book` and `Review`:
     - `Book` is an entity with a one-to-many relationship to `Review`.
     - Use SQLAlchemy's `relationship()` and `ForeignKey` to define the relationship.
  2. Implement and test:
     - Fix issues in the `update_review` method in the `routes.reviews.py` to ensure proper handling of relationships.
  3. Update the routes in `routes/reviews.py` to support CRUD operations for reviews.
  4. Test CRUD operations for both `Book` and `Review` entities using Swagger UI or the REST Client:
     - POST `/books/{id}/reviews`
     - GET `/books/{id}/reviews`


- **Notes**:
  - Use Alembic to manage migrations for new tables (e.g., `reviews` table).
  - Verify the relationship schema and data using SQLite Viewer.

---

### ** Activity 3: Exploring ChromaDB and AI Integration**

### **Objective**
The goal of this activity is to:
1. Learn how to add and query data in ChromaDB.
2. Understand the difference between raw list-style search results and AI-enhanced natural language summaries.

---

### **Step 1: Add Books to ChromaDB**

1. **Endpoint**: `POST chroma/`
2. **Description**: Add a book's title and description to ChromaDB, where embeddings will be generated for semantic search.

3. **Instructions**:
   - Use the following sample data to add books:

     **Example 1**:
     ```http
     POST /chroma
     Content-Type: application/json

     {
         "book_id": "1",
         "title": "Deep Learning for Natural Language Processing",
         "description": "This comprehensive book provides an in-depth overview of deep learning techniques tailored for natural language processing (NLP). Starting with foundational concepts in deep learning and their applications to NLP, the book delves into the implementation of neural networks, recurrent networks, and attention mechanisms like transformers. It covers practical examples, such as building machine translation systems, text summarizers, and sentiment analysis tools. Advanced topics like GPT-based models and fine-tuning BERT for specific tasks are also explored. Each chapter includes hands-on exercises to reinforce theoretical concepts, making it ideal for both beginners and seasoned professionals in the field of NLP."
     }
     ```

     **Example 2**:
     ```http
     POST /chroma
     Content-Type: application/json

     {
         "book_id": "2",
         "title": "Python Programming for Data Science and Machine Learning",
         "description": "This book serves as a comprehensive guide to using Python for data science and machine learning. Readers will learn how to process and visualize data using libraries like NumPy, Pandas, and Matplotlib. It covers essential machine learning algorithms such as linear regression, decision trees, clustering, and support vector machines, along with detailed explanations of their implementation in Python. Advanced topics include neural networks with TensorFlow and PyTorch, natural language processing, and deep learning techniques. Each chapter provides real-world datasets for hands-on projects, ranging from building recommendation systems to predictive analytics. Designed for data enthusiasts, the book bridges the gap between theory and practical implementation."
     }
     ```

4. **Expected Response**:
   ```json
   {
       "message": "Book 'Deep Learning for Natural Language Processing' added to ChromaDB successfully."
   }
   ```

---

### **Step 2: Search for Books with Raw List-Style Response**

1. **Endpoint**: `chromachroma/similarities`
2. **Description**: Search for books based on a query and see the raw list-style response with metadata.

3. **Concept: Distance Score**:
   - The **distance score** measures the difference between the query and stored embeddings in ChromaDB.
   - **Range**:
     - For cosine similarity, distance typically ranges between `0` (most similar) and `2` (least similar). However, practical values are usually between `0` and `1`.
   - **Smaller values indicate higher similarity**.
   - Use the `distance_threshold` parameter to filter results. For example:
     - `distance_threshold = 0.2`: Only very similar results are returned.
     - `distance_threshold = 1.0`: Includes broader matches.

4. **Instructions**:
   - Make a search query:
     ```http
     GET chroma/similarities?query=Deep Learning&distance_threshold=1.0
     ```
   - Examine the returned response, which includes:
     - Metadata (title and description).
     - Distance scores for each result.

5. **Expected Response**:
   ```json
   {
   "query": "Deep Learning",
   "response": [
      {
         "description": "This comprehensive book provides an in-depth overview of deep learning techniques tailored for natural language processing (NLP). Starting with foundational concepts in deep learning and their applications to NLP, the book delves into the implementation of neural networks, recurrent networks, and attention mechanisms like transformers. It covers practical examples, such as building machine translation systems, text summarizers, and sentiment analysis tools. Advanced topics like GPT-based models and fine-tuning BERT for specific tasks are also explored. Each chapter includes hands-on exercises to reinforce theoretical concepts, making it ideal for both beginners and seasoned professionals in the field of NLP.",
         "title": "Deep Learning for Natural Language Processing",
         "distance": 0.8939606134347404
      }
   ]
   }
   ```

---

### **Step 3: Search with AI-Enhanced Summary**

1. **Endpoint**: `chroma/summary`
2. **Description**: Search for books and retrieve a natural language summary using OpenAI.

3. **Concept: AI-Enhanced Summaries**:
   - The `chroma/summary` endpoint uses OpenAI's GPT model to convert the raw response into a natural language summary.
   - It summarizes:
     - The number of matching books.
     - Each book's title and a brief description.

4. **Instructions**:
   - Make the same search query:
     ```http
     GET chroma/summary?query=Deep Learning&distance_threshold=1.0
     ```
   - Compare the response to the raw list-style response from `chroma/similarities`.

5. **Expected Response**:
   ```json
   {
   "query": "Deep Learning",
   "response": "**Number of Books Found:** 1\n\n1. **Deep Learning for Natural Language Processing**  \n   This book offers a comprehensive overview of deep learning techniques specifically for natural language processing (NLP). It covers foundational concepts, neural networks, recurrent networks, and attention mechanisms like transformers. Practical examples include machine translation, text summarization, and sentiment analysis. Advanced topics such as GPT models and fine-tuning BERT are also discussed, with hands-on exercises included to reinforce learning, making it suitable for both beginners and experienced professionals in NLP."
   }
   ```

---

### **Key Differences Between `chroma/similarities` and `chroma/summary`**

| **Feature**         | **chroma/similarities**                               | **chroma/summary**                                    |
|----------------------|---------------------------------------------------|--------------------------------------------------|
| Response Type        | Raw JSON with metadata and distance scores        | Natural language summary of search results       |
| Distance Scores      | Explicitly included in the response               | Not shown directly, used internally for ranking |
| User-Friendly Output | Minimal formatting                                | Designed for user readability                    |

---

---

### **Comparison and Insights**

1. **Raw List-Style Response**:
   - Provides structured data (metadata) directly from the database.
   - Useful for detailed programmatic access or analysis.

2. **AI-Enhanced Summary**:
   - Converts raw data into human-readable text.
   - Useful for user-facing applications where clarity and conciseness are essential.

---

### **Additional Tasks for Students**

1. Add more books to ChromaDB using `POST /chroma` and repeat the search queries with more complex keywords.
2. Modify the `distance_threshold` parameter to observe how it affects the results.
   - For example:
     - `distance_threshold=0.5` will show more highly related books.
     - `distance_threshold=0.9` will show only loosly relevant books.
3. Experiment with the prompt in the `generate_natural_language_response` function to customize the AI's response style.

---

