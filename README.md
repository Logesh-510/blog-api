# Blog Management API

A backend REST API for a mini blogging platform built with **FastAPI**, **SQLAlchemy**, and **SQLite**.

The API provides JWT authentication, blog post management, comments, likes/unlikes, image uploads, pagination and search, subscription-based access control, billing history, email notifications, post view tracking, and a user dashboard with interactive analytics.

## Features

* User registration
* Secure password hashing with bcrypt
* JWT-based authentication
* Login using username or email
* Protected API endpoints
* Get current authenticated user
* Create blog posts
* View all posts
* View a single post
* Update own posts
* Delete own posts
* Ownership-based authorization
* Multiple image uploads per post
* Post image serving through `/media`
* Pagination for posts
* Search posts by title/content
* Add comments to posts
* View post comments publicly
* Like and unlike posts
* Prevent duplicate likes
* Subscription plans
* Plan-based post, image, like, and comment limits
* Basic, Premium, and Pro subscription plans
* Billing history
* Subscription limit validation
* Email notification for new comments
* Email notification for new likes
* Post view tracking
* User dashboard API
* Dashboard statistics and analytics
* Chart.js visualization
* Per-post likes and comments chart
* Responsive dashboard UI
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
| Chart.js         | Dashboard data visualization    |
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
│       ├── likes.py
│       ├── subscriptions.py
│       └── dashboard.py
│
├── dashboard/
│   └── dashboard.html
│
├── media/
│   ├── posts/
│   │   └── .gitkeep
│   └── invoices/
│       └── .gitkeep
│
├── .env
├── .gitignore
├── requirements.txt
├── README.md
└── Blog_Management_API_Postman_Collection.json
```

> `.env`, `blog.db`, `venv/`, uploaded images, and generated invoices should not be committed to GitHub.

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
* Upload post images
* Update/delete posts
* Search and paginate posts
* Add comments
* Like/unlike posts
* Manage subscriptions
* View dashboard statistics
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

Login supports either username or email.

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

Post creation supports one or more image uploads.

### Get All Posts

```http
GET /posts/
```

Public endpoint.

Supports pagination and search.

Example:

```text
GET /posts/?page=1&limit=10
```

Example search:

```text
GET /posts/?search=FastAPI
```

### Get Single Post

```http
GET /posts/{post_id}
```

Public endpoint.

Each successful request tracks a post view.

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

## Subscription & Billing

The API provides subscription-based access control.

### Subscription Plans

Available plans:

| Plan    | Price | Max Posts | Max Images/Post | Max Likes | Max Comments |
| ------- | ----: | --------: | --------------: | --------: | -----------: |
| Basic   |    99 |         1 |               1 |         5 |            5 |
| Premium |   199 |         2 |               2 |        20 |           20 |
| Pro     |   399 | Unlimited |       Unlimited | Unlimited |    Unlimited |

### View Available Plans

```http
GET /subscriptions/plans
```

### View Current Subscription

```http
GET /subscriptions/current
```

Authentication required.

### Subscription Limits

When a user reaches their subscription limit, the API returns:

```text
You've reached your plan limit. Kindly upgrade your plan to continue.
```

Users without an active subscription cannot create posts.

### Billing History

Subscription and payment information is stored in the billing history table.

## User Dashboard

The application provides a user dashboard for personal activity statistics and analytics.

### Dashboard API

```http
GET /user/dashboard/
```

Authentication required.

The dashboard returns:

* Total posts created
* Total comments made
* Total likes received on the user's posts
* Total views received on the user's posts
* Per-post likes
* Per-post comments

Each authenticated user can only access their own dashboard data.

### Dashboard UI

The dashboard is available at:

```text
http://127.0.0.1:8000/dashboard
```

The dashboard uses **Chart.js** to display:

* Total Posts
* Total Comments
* Total Likes
* Total Views
* Likes and Comments per Post

Dashboard data is loaded dynamically from the authenticated dashboard API.

## Post View Tracking

Post views are tracked automatically.

Whenever a user successfully requests:

```http
GET /posts/{post_id}
```

the post's view count is incremented.

The total views for a user's posts are displayed in the User Dashboard.

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

Dashboard data is also protected using JWT authentication, ensuring users can only access their own activity statistics.

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
* Subscription limit reached
* Missing active subscription

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

Main tables include:

* `users`
* `posts`
* `post_images`
* `comments`
* `likes`
* `subscription_plans`
* `billing_history`

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
* User-specific dashboard access
* Subscription-based access control

## Testing

The API was tested using Swagger UI and Postman.

A Postman collection containing API requests and error-handling tests is included in the repository.

Tested functionality includes:

* User registration
* Login with username
* Login with email
* JWT authentication
* Current-user endpoint
* Public post access
* Post creation
* Post update
* Post deletion
* Ownership restrictions
* Multiple image uploads
* Pagination
* Post search
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
* Subscription plans
* Current subscription
* Subscription limit enforcement
* User dashboard statistics
* Dashboard JWT protection
* Post view tracking
* Chart.js dashboard visualization

### Postman Collection

The Postman collection is available in the project root:

`Blog_Management_API_Postman_Collection.json`

It includes requests for:

* Authentication
* Post CRUD operations
* Image uploads
* Pagination and search
* Comments
* Likes and unlikes
* Duplicate-like validation
* Ownership authorization
* Subscription and billing APIs
* Dashboard API
* Authentication and validation errors
