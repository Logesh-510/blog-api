# Blog Management API

A backend REST API for a mini blogging platform built with **FastAPI**, **SQLAlchemy**, and **SQLite**.

The API provides JWT authentication, blog post management, comments, likes/unlikes, ownership protection, input validation, and email notifications.

## Features

* User registration
* Secure password hashing with bcrypt
* JWT-based authentication
* Protected API endpoints
* Get current authenticated user
* Create blog posts
* View all posts
* View a single post
* Update own posts
* Delete own posts
* Ownership-based authorization
* Add comments to posts
* View post comments publicly
* Like and unlike posts
* Prevent duplicate likes
* Email notification for new comments
* Email notification for new likes
* Input validation with Pydantic
* Proper HTTP error handling
* SQLite database with SQLAlchemy ORM
* Interactive Swagger API documentation
* Environment variable configuration
* Dependency management with `requirements.txt`

## Tech Stack

| Technology       | Purpose                         |
| ---------------- | ------------------------------- |
| Python           | Programming language            |
| FastAPI          | Backend REST API framework      |
| SQLAlchemy       | ORM and database operations     |
| SQLite           | Database                        |
| Pydantic         | Request/response validation     |
| JWT              | Authentication                  |
| Passlib + bcrypt | Password hashing                |
| Python-dotenv    | Environment variable management |
| SMTP             | Email notifications             |
| Uvicorn          | ASGI server                     |
| Swagger UI       | API testing and documentation   |

## Project Structure

```text
blog-api/
│
├── app/
│   ├── __init__.py
│   ├── auth.py
│   ├── database.py
│   ├── dependencies.py
│   ├── email.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   │
│   └── routers/
│       ├── __init__.py
│       ├── auth.py
│       ├── posts.py
│       ├── comments.py
│       └── likes.py
│
├── .env
├── .gitignore
├── requirements.txt
├── README.md
└── Blog_Management_API_Postman_Collection.json
```

> `.env`, `blog.db`, and `venv/` should not be committed to GitHub.

## Installation

### 1. Clone the repository

```bash
git clone <your-github-repository-url>
cd blog-api
```

### 2. Create a virtual environment

Windows:

```powershell
python -m venv venv
```

### 3. Activate the virtual environment

```powershell
venv\Scripts\activate
```

### 4. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the project root:

```env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USERNAME=your-email@gmail.com
EMAIL_PASSWORD=your-gmail-app-password
SECRET_KEY=your-secret-key
```

### Important

Never commit your `.env` file to GitHub.

For Gmail SMTP, use a **Gmail App Password** rather than your normal Gmail password.

## Run the Application

From the project directory:

```powershell
python -m uvicorn app.main:app --reload
```

The API will run at:

```text
http://127.0.0.1:8000
```

## API Documentation

FastAPI automatically provides interactive Swagger documentation.

Open:

```text
http://127.0.0.1:8000/docs
```

You can use Swagger UI to:

* Register users
* Login
* Authorize with JWT
* Create posts
* Update/delete posts
* Add comments
* Like/unlike posts
* Test validation and authorization errors

OpenAPI JSON:

```text
http://127.0.0.1:8000/openapi.json
```

## Authentication

### Register

```http
POST /auth/register
```

Example request:

```json
{
  "username": "logesh",
  "email": "logesh@example.com",
  "password": "password123"
}
```

### Login

```http
POST /auth/login
```

The login endpoint returns a JWT access token.

Use the token in protected requests:

```text
Authorization: Bearer <access_token>
```

### Current User

```http
GET /auth/me
```

Returns the currently authenticated user.

## Posts API

### Create Post

```http
POST /posts/
```

Authentication required.

### Get All Posts

```http
GET /posts/
```

Public endpoint.

### Get Single Post

```http
GET /posts/{post_id}
```

Public endpoint.

### Update Post

```http
PUT /posts/{post_id}
```

Authentication required.

Only the post owner can update the post.

### Delete Post

```http
DELETE /posts/{post_id}
```

Authentication required.

Only the post owner can delete the post.

## Comments API

### Add Comment

```http
POST /posts/{post_id}/comments/
```

Authentication required.

When a comment is created, an email notification is sent to the post owner.

### Get Comments

```http
GET /posts/{post_id}/comments/
```

Public endpoint.

## Likes API

### Like Post

```http
POST /posts/{post_id}/like/
```

Authentication required.

A user cannot like the same post multiple times.

When a post receives a new like, an email notification is sent to the post owner.

### Unlike Post

```http
DELETE /posts/{post_id}/like/
```

Authentication required.

## Authorization

The API implements ownership protection for posts.

For example, if User A creates a post, User B cannot:

* Update User A's post
* Delete User A's post

The API returns:

```text
403 Forbidden
```

with an appropriate error message.

## Validation

Request data is validated using Pydantic.

Examples of validation rules:

* Username: 3–50 characters
* Password: 6–100 characters
* Email: valid email format
* Post title: 3–200 characters
* Post content: minimum 10 characters
* Comment text: 1–1000 characters

Invalid input returns:

```text
422 Unprocessable Entity
```

## Error Handling

The API handles common errors such as:

```text
400 Bad Request
401 Unauthorized
403 Forbidden
404 Not Found
422 Unprocessable Entity
```

Examples:

* Invalid login credentials
* Invalid JWT token
* Unauthenticated protected requests
* Post not found
* Unauthorized post modification
* Duplicate like
* Unlike without an existing like

## Email Notifications

The API uses Gmail SMTP to send notifications.

Notifications are sent when:

1. A user comments on a post.
2. A user likes a post.

Email credentials are loaded from `.env` using `python-dotenv`.

## Database

The application uses SQLite with SQLAlchemy ORM.

Database file:

```text
blog.db
```

Main tables:

* `users`
* `posts`
* `comments`
* `likes`

Relationships are configured using SQLAlchemy ORM.

## Security

Security-related features include:

* Password hashing using bcrypt
* JWT authentication
* Protected endpoints
* Ownership authorization
* Secret key stored in environment variables
* Email credentials stored in environment variables
* `.env` excluded from Git
* Invalid JWT rejection

## Testing

The API was tested using Swagger UI and Postman.
A Postman collection containing the API requests and error-handling tests is included in the repository.

Tested functionality includes:

* User registration
* Login
* JWT authentication
* Current-user endpoint
* Public post access
* Post creation
* Post update
* Post deletion
* Ownership restrictions
* Public comments
* Comment validation
* Comment notifications
* Likes
* Duplicate-like prevention
* Unlike
* Invalid post handling
* Authentication failures
* Invalid JWT handling
* Email notifications
* Dependency installation
  
### Postman Collection

The Postman collection is available in the project root:

`Blog_Management_API_Postman_Collection.json`

It includes requests for:

- Authentication
- Post CRUD operations
- Comments
- Likes and unlikes
- Duplicate-like validation
- Ownership authorization
- Authentication and validation errors
