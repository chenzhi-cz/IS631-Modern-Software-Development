### **Week 5 Security Lab using FastAPI, AWS Cognito, and JWT**

---

#### **1. Before Class (Individual)**

- **Preview**: Learn Pydantic, AWS Cognito concept and operation.


---
### **Lab Activity: Exploring Pydantic Validation in FastAPI**

This lab activity will guide students to explore **Pydantic** validation in FastAPI using the updated book-related code. Students will also practice adding similar validation to the review-related code.

---

### **Objective**

1. Understand how Pydantic is used for validation in FastAPI.
2. Test book-related APIs with validation rules for edge cases.
3. Apply similar validation rules to review-related models and APIs.

---

### **Activity 1: Testing Validation for Book APIs**

#### **Instructions**

1. Open the `models/book.py` file and review the validation rules applied to the `BookBase` model:
   - `title`: Minimum 3 characters, maximum 100 characters.
   - `author`: Minimum 3 characters, maximum 50 characters.
   - `year`: Positive integer.
   - `description`: Required, minimum 10 characters, maximum 1000 characters.

2. Use the following two test cases to validate the behavior of the `POST /books` API.

---

#### **Test Case 1: Invalid Input**

Use an invalid book payload with missing and incorrect fields.

**Request**:
```json
{
    "title": "A",
    "author": "X",
    "year": -2023,
    "description": "Too short"
}
```

**Expected Response**:
```json
{
  "detail": [
    {
      "type": "string_too_short",
      "loc": [
        "body",
        "title"
      ],
      "msg": "String should have at least 3 characters",
      "input": "A",
      "ctx": {
        "min_length": 3
      }
    },
    {
      "type": "string_too_short",
      "loc": [
        "body",
        "author"
      ],
      "msg": "String should have at least 3 characters",
      "input": "X",
      "ctx": {
        "min_length": 3
      }
    },
    {
      "type": "greater_than",
      "loc": [
        "body",
        "year"
      ],
      "msg": "Input should be greater than 0",
      "input": -2023,
      "ctx": {
        "gt": 0
      }
    },
    {
      "type": "string_too_short",
      "loc": [
        "body",
        "description"
      ],
      "msg": "String should have at least 10 characters",
      "input": "Too Short",
      "ctx": {
        "min_length": 10
      }
    }
  ]
}
```

---

#### **Test Case 2: Valid Input**

Use a valid book payload.

**Request**:
```json
{
    "title": "FastAPI Essentials",
    "author": "John Doe",
    "year": 2023,
    "description": "This book provides an excellent guide to mastering FastAPI."
}
```

**Expected Response**:
```json
{
    "id": 1,
    "title": "FastAPI Essentials",
    "author": "John Doe",
    "year": 2023,
    "description": "This book provides an excellent guide to mastering FastAPI."
}
```

---

### **Activity 2: Student Activity – Add Validation for Reviews**

#### **Instructions**

1. Open the `models/review.py` file.
2. Add validation rules to the `ReviewBase` model:
   - `review`: Required, minimum 10 characters, maximum 500 characters.
3. Test the review-related APIs:
   - Provide a payload with a review shorter than 10 characters and observe the error.
   - Provide a valid review and ensure it gets added successfully.

---

#### **Hints for Review Validation**

**Example Validation for Reviews**:
```python
from pydantic import BaseModel, Field

class ReviewBase(BaseModel):
    review: str = Field(..., min_length=10, max_length=500, description="The review content (10-500 characters)")
```

---

### **Expected Learning Outcomes**

1. Understand how to use Pydantic to validate input data in FastAPI.
2. Recognize how validation improves data integrity and security.
3. Apply similar validation techniques across different parts of the application.

### **Activity 3: Setting Up AWS Cognito User Pool and Users**

In this activity, students will learn how to create and configure an AWS Cognito User Pool, set up user groups, create users, and confirm them using the AWS Management Console and CLI. This setup will serve as a foundation for integrating authentication and authorization into their FastAPI application.

---

### **Objective**
1. Set up an AWS Cognito User Pool and a Client App (`books_app`).
2. Create user groups (`Users` and `Admins`).
3. Add users to the respective groups.
4. Confirm the users and set their passwords as permanent.

---

### **Step-by-Step Instructions**

#### **1. Register for AWS**
- Go to [AWS Console](https://aws.amazon.com/console/).
- Sign in or register for a free tier account if you don’t have one.

---

#### **2. Create a Cognito User Pool**
1. Open the **Cognito** service in AWS.
2. Click on **Create User Pool**.
3. **Configure the user pool**:
   - Name: `books_user_pool`.
   - Attributes: Include `username` and optionally `email`.
4. **Set up password policy**:
   - Minimum password length: `8`.
   - Enable special characters.
5. Save and create the user pool.

---

#### **3. Create an App Client**
1. In the User Pool dashboard, go to **App Integration > App Clients**.
2. Click on **Add an App Client**.
3. Configure the app client:
   - Name: `books_app`.
   - Enable **USER_PASSWORD_AUTH**.
4. Save the client and note the **App Client ID**.

---

#### **4. Create User Groups**
1. In the User Pool dashboard, go to **Groups**.
2. Create the following groups:
   - **Users**: For general users who can access basic functionality.
   - **Admins**: For administrators who have elevated privileges.
3. Save the groups.

---

#### **5. Create Users**
1. In the User Pool dashboard, go to **Users**.
2. Create two users:
   - **User 1**:
     - Username: `user1`.
     - Email: Optional (e.g., `user1@example.com`).
   - **User 2**:
     - Username: `admin1`.
     - Email: Optional (e.g., `admin1@example.com`).
3. Leave the status as unconfirmed (it will be updated in the next step).

---

#### **6. Add Users to Groups**
1. Go to the **Groups** section of your user pool.
2. Select the `Users` group and add `user1` to it.
3. Select the `Admins` group and add `admin1` to it.

---


### **Using AWS CloudShell**

1. **Open AWS CloudShell**:
   - Navigate to the AWS Management Console.
   - Click on the **CloudShell** icon in the top-right menu bar (it looks like a terminal).

2. **Run Commands Directly**:
   Since CloudShell already has the AWS CLI installed and configured, you can immediately run the required commands, such as:
   - **Check the status of users**:
     ```bash
     aws cognito-idp list-users --user-pool-id <USER_POOL_ID>
     ```
   - **Set passwords and confirm users**:
     ```bash
     aws cognito-idp admin-set-user-password \
         --user-pool-id <USER_POOL_ID> \
         --username user1 \
         --password UserPass123! \
         --permanent

     aws cognito-idp admin-set-user-password \
         --user-pool-id <USER_POOL_ID> \
         --username admin1 \
         --password AdminPass123! \
         --permanent
     ```

3. Verify the users are confirmed:
   ```bash
   aws cognito-idp list-users --user-pool-id <USER_POOL_ID>
   ```
---

### **Expected Results**
1. **User Pool**: `books_user_pool` with proper configurations.
2. **App Client**: `books_app` created and connected to the User Pool.
3. **Groups**: Two groups named `Users` and `Admins`.
4. **Users**:
   - `user1`: Confirmed and part of the `Users` group.
   - `admin1`: Confirmed and part of the `Admins` group.

---

### **Learning Outcomes**
1. Understand the process of setting up an AWS Cognito User Pool and App Client.
2. Learn how to use AWS CLI to manage users programmatically.
3. Recognize the importance of groups and roles for managing application security.


### **Activity 4: Configuring and Testing Authentication and Authorization with AWS Cognito**

In this activity, students will:
1. Configure their FastAPI project to use AWS Cognito by setting up the `.env` file.
2. Explore the code handling authentication and role-based authorization.
3. Test authentication and authorization using **Swagger UI**.

---

### **Objective**
- Set up AWS Cognito in the FastAPI project.
- Understand the implementation of authentication and role-based authorization.
- Test restricted APIs using **Swagger UI** with access tokens.

---

### **Step-by-Step Instructions**

#### **1. Configure the `.env` File**
Students need to retrieve the following AWS Cognito values from the AWS Console:
- **Region**: The region where the user pool was created (e.g., `ap-southeast-2`).
- **User Pool ID**: Found in the **Cognito User Pool** dashboard.
- **App Client ID**: Found in the **App Integration** section under **App Clients**.
- **App Client Secret**: Found in the same place as the App Client ID.

**Example `.env` File**:
```env
COGNITO_REGION=ap-southeast-2
COGNITO_USER_POOL_ID=ap-southeast-2_dxxxxxx
COGNITO_CLIENT_ID=ld31q9g00uonlq61fvbxxxxxx
COGNITO_CLIENT_SECRET=ql37f5tib2t78nvtq86pgramo0c52rphvrfginfxxxxxxxxxxxx
```

Save the file in the root directory of your FastAPI project.

---

#### **2. Review the Code**

1. **Authentication Code**:
   Open the `services/cognito_service.py` file and review the `authenticate_user` function. This function:
   - Authenticates the user using their username and password.
   - Exchanges the credentials for tokens (ID token, access token, refresh token) from AWS Cognito.

2. **Login API**:
   Open the `routes/auth.py` file and review the login endpoint:
   ```python
   @router.post("/login")
   def login(username: str, password: str):
   ```

3. **Role-Based Authorization**:
   Look at the `POST /books/{book_id}/reviews` route in `routes/reviews.py`, which now includes a role authorization check.

---

#### **3. Test the APIs in Swagger UI**

1. **Start the Application**:
   Start the FastAPI application:
   ```bash
   uvicorn app.main:app --reload
   ```
   Open Swagger UI at:
   ```
   http://127.0.0.1:8000/docs
   ```

2. **Call `POST /books/{book_id}/reviews` Without Logging In**:
   - Go to the `POST /books/{book_id}/reviews` endpoint in Swagger UI.
   - Set `book_id` to an existing book (e.g., `1`) and provide a review payload:
     ```json
     {
         "review": "Amazing book!"
     }
     ```
   - Click **Execute**.

   **Expected Response**:
   ```json
   {
       "detail": "Not authenticated"
   }
   ```

   This shows that the API is protected and requires authentication.

3. **Login to Get an Access Token**:
   - Navigate to the `POST /login` endpoint in Swagger UI.
   - Enter your credentials (e.g., `user1` and `UserPass123!`).
   - Click **Execute**.

   **Expected Response**:
   ```json
   {
       "message": "Login successful",
       "tokens": {
           "id_token": "eyJraWQiOiJ...",
           "access_token": "eyJraWQiOiJ...",
           "refresh_token": "eyJjdHkiOiJ..."
       }
   }
   ```
   Copy the value of key `access_token`.

4. **Authorize in Swagger UI**:
   - Click the **Authorize** button in the top-right corner of Swagger UI.
   - Enter the access token in the following format:
     ```
     Bearer <access_token>
     ```
   - Click **Authorize**, then **Close**.

5. **Call `POST /books/{book_id}/reviews` With the Token**:
   - Go back to the `POST /books/{book_id}/reviews` endpoint.
   - Enter the same payload:
     ```json
     {
         "review": "Amazing book!"
     }
     ```
   - Click **Execute**.

   **Expected Response**:
   ```json
   {
       "id": 1,
       "book_id": 1,
       "review": "Amazing book!"
   }
   ```

6. **Verify the Added Review**:
   - Navigate to the `GET /books/{book_id}/reviews` endpoint.
   - Enter the same `book_id` (e.g., `1`).
   - Click **Execute**.

   **Expected Response**:
   ```json
   [
       {
           "id": 1,
           "book_id": 1,
           "review": "Amazing book!"
       }
   ]
   ```
---

### **Learning Outcomes**
1. Understand how AWS Cognito integrates with FastAPI for authentication.
2. Learn how role-based authorization is implemented in FastAPI.
3. Experience API testing using Swagger UI with bearer tokens.


### **Activity 5: Enforcing Role-Based Authorization for Books APIs**

In this activity, students will enforce role-based access control for APIs that manage books. Only users in the `Admins` group will be allowed to add or delete books.

---

#### **Objective**
1. Add role-based authorization to the `POST /books` and `DELETE /books/{book_id}` APIs.
2. Test the APIs using different user roles (`Admins` and `Users`) and observe the behavior.

---
#### **Instructions**

1. **Add Role Requirements for Books APIs**:
   - Use the `check_user_role` function with the `CognitoAdminRole` (defined in `.env` as `Admins`).
   - Update the routes for:
     - **`POST /books`**: Allow only admins to add books.
     - **`DELETE /books/{book_id}`**: Allow only admins to delete books.

**Updated Routes**:

**`POST /books`**:
```python
@router.post("/books", response_model=BookResponse)
```

**`DELETE /books/{book_id}`**:
```python
@router.delete("/books/{book_id}")
```

2. **Test the APIs**:
   - **Without Logging In**:
     - Call the `POST /books` and `DELETE /books/{book_id}` APIs in Swagger UI.
     - Confirm the response shows a `403 Forbidden` error with a "Not authenticated" message.
   - **As a User**:
     - Log in as `user1`, authorize in Swagger UI, and test the APIs.
     - Confirm the response shows a `403 Forbidden` error with a "Admin permissions required" message.
   - **As an Admin**:
     - Log in as `admin1`, authorize in Swagger UI, and test the APIs.
     - Confirm:
       - The `POST /books` API successfully adds a book.
       - The `DELETE /books/{book_id}` API successfully deletes a book.
---

