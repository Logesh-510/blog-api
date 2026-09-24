# Blog Management API

A backend REST API for a mini blogging platform built with **FastAPI**, **SQLAlchemy**, and **SQLite**.

The application provides JWT authentication, blog post management, comments, likes/unlikes, image uploads, pagination and search, subscription-based access control, billing history, email notifications, an in-app notification center, post view tracking, and a user dashboard with interactive analytics.

A separate **React/Vite frontend** is also included for the In-App Notification Center.

---

## Features

### Authentication & Security

* User registration
* Secure password hashing with bcrypt
* JWT-based authentication
* Login using username or email
* Protected API endpoints
* Get current authenticated user
* Ownership-based authorization
* Invalid JWT rejection
* Environment variable configuration

### Blog Posts

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
* Post view tracking

### Comments & Likes

* Add comments to posts
* View post comments publicly
* Like and unlike posts
* Prevent duplicate likes
* Comment activity notifications
* Like activity notifications

### Subscription & Billing

* Subscription plans
* Basic, Premium, and Pro plans
* Plan-based post limits
* Plan-based image limits
* Plan-based like limits
* Plan-based comment limits
* Subscription activation
* Subscription renewal
* Billing history
* Subscription limit validation
* Invoice generation

### Email Notifications

* Email notification when someone comments on a post
* Email notification when someone likes a post
* SMTP-based email delivery
* Gmail App Password support
* Environment-based email configuration

### In-App Notification Center

* Notification model with user-specific notifications
* Like notifications
* Comment notifications
* Subscription activation notifications
* Subscription renewal notifications
* Notification type identification
* Read/unread notification state
* Unread notification badge
* Individual notification read/unread toggle
* Mark all notifications as read
* Notification timestamps
* Notification icons
* Notification type labels
* User-specific notification filtering
* Automatic notification refresh using 10-second polling
* Responsive notification dropdown
* Login/logout support
* JWT-based frontend authentication
* Persistent authentication using browser local storage

### User Dashboard

* User-specific dashboard
* Total posts
* Total comments
* Total likes received
* Total views
* Per-post likes
* Per-post comments
* Chart.js visualization
* Responsive dashboard UI

### API & Validation

* Input validation with Pydantic
* Proper HTTP error handling
* SQLite database with SQLAlchemy ORM
* Interactive Swagger API documentation
* Postman API testing
* Dependency management with `requirements.txt`

---

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
| React            | Notification Center frontend    |
| Vite             | React development/build tool    |
| Lucide React     | Notification UI icons           |
| Uvicorn          | ASGI server                     |
| Swagger UI       | API testing and documentation   |
| Postman          | API testing                     |

---

## Project Structure

```text
blog-api/
│
├── app/
│   ├── __init__.py
│   ├── auth.py
│   ├── database.py
│   ├── dependencies.py
│   ├── email_service.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   │
│   ├── services/
│   │   └── notification_service.py
│   │
│   └── routers/
│       ├── __init__.py
│       ├── auth.py
│       ├── posts.py
│       ├── comments.py
│       ├── likes.py
│       ├── subscriptions.py
│       ├── dashboard.py
│       └── notifications.py
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
├── blog-notification-frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── ...
│   ├── package.json
│   ├── package-lock.json
│   └── index.html
│
├── .env
├── .gitignore
├── requirements.txt
├── README.md
└── Blog_Management_API_Postman_Collection.json
```

> `.env`, `blog.db`, `venv/`, uploaded images, generated invoices, and frontend `node_modules/` should not be committed to GitHub.

---

## Installation

### 1. Clone the Repository

```bash
git clone <your-github-repository-url>

cd blog-api
```

### 2. Create a Virtual Environment

Windows:

```powershell
python -m venv venv
```

### 3. Activate the Virtual Environment

```powershell
venv\Scripts\activate
```

### 4. Install Backend Dependencies

```powershell
python -m pip install -r requirements.txt
```

---

## Frontend Installation

The In-App Notification Center frontend is located inside:

```text
blog-notification-frontend/
```

Navigate to the frontend directory:

```powershell
cd blog-notification-frontend
```

Install the Node.js dependencies:

```powershell
npm install
```

The frontend uses **React**, **Vite**, and **Lucide React**.

---

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

---

# Run the Backend

From the project directory:

```powershell
python -m uvicorn app.main:app --reload
```

The API will run at:

```text
http://127.0.0.1:8000
```

---

# Run the Notification Center Frontend

Open another terminal:

```powershell
cd C:\Users\Welcome\blog-api\blog-notification-frontend
```

Run the React development server:

```powershell
npm run dev
```

The frontend will normally run at:

```text
http://localhost:5173
```

The frontend communicates with the FastAPI backend running at:

```text
http://127.0.0.1:8000
```

---

# API Documentation

FastAPI automatically provides interactive Swagger documentation.

Open:

```text
http://127.0.0.1:8000/docs
```

Swagger UI can be used to:

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
* View billing information
* View dashboard statistics
* View notifications
* Mark notifications as read/unread
* Mark all notifications as read
* Test validation and authorization errors

OpenAPI JSON:

```text
http://127.0.0.1:8000/openapi.json
```

---

# Authentication

## Register

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

## Login

```http
POST /auth/login
```

The login endpoint returns a JWT access token.

Login supports either username or email.

Use the token in protected requests:

```text
Authorization: Bearer <access_token>
```

## Current User

```http
GET /auth/me
```

Returns the currently authenticated user.

---

# Posts API

## Create Post

```http
POST /posts/
```

Authentication required.

Post creation supports one or more image uploads.

## Get All Posts

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

## Get Single Post

```http
GET /posts/{post_id}
```

Public endpoint.

Each successful request tracks a post view.

## Update Post

```http
PUT /posts/{post_id}
```

Authentication required.

Only the post owner can update the post.

## Delete Post

```http
DELETE /posts/{post_id}
```

Authentication required.

Only the post owner can delete the post.

---

# Comments API

## Add Comment

```http
POST /posts/{post_id}/comments/
```

Authentication required.

When a comment is created:

* An email notification is sent to the post owner.
* An in-app notification is created for the post owner.

## Get Comments

```http
GET /posts/{post_id}/comments/
```

Public endpoint.

---

# Likes API

## Like Post

```http
POST /posts/{post_id}/like/
```

Authentication required.

A user cannot like the same post multiple times.

When a post receives a new like:

* An email notification is sent to the post owner.
* An in-app notification is created for the post owner.

## Unlike Post

```http
DELETE /posts/{post_id}/like/
```

Authentication required.

---

# Subscription & Billing

The API provides subscription-based access control.

## Subscription Plans

Available plans:

| Plan    | Price | Max Posts | Max Images/Post | Max Likes | Max Comments |
| ------- | ----: | --------: | --------------: | --------: | -----------: |
| Basic   |    99 |         1 |               1 |         5 |            5 |
| Premium |   199 |         2 |               2 |        20 |           20 |
| Pro     |   399 | Unlimited |       Unlimited | Unlimited |    Unlimited |

## View Available Plans

```http
GET /subscriptions/plans
```

## View Current Subscription

```http
GET /subscriptions/current
```

Authentication required.

## Subscription Limits

When a user reaches their subscription limit, the API returns:

```text
You've reached your plan limit. Kindly upgrade your plan to continue.
```

Users without an active subscription cannot create posts.

## Billing History

Subscription and payment information is stored in the billing history table.

Invoices are generated and stored under:

```text
/media/invoices/
```

---

# User Dashboard

The application provides a user dashboard for personal activity statistics and analytics.

## Dashboard API

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

## Dashboard UI

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

---

# In-App Notification Center

The project includes a separate React/Vite frontend for an interactive notification center.

Frontend URL:

```text
http://localhost:5173
```

## Notification Features

The notification center provides:

* Bell notification icon
* Unread notification badge
* Notification dropdown
* Recent notifications
* Notification type labels
* Notification type icons
* Friendly timestamps
* Unread notification highlighting
* Unread indicator dot
* Individual read/unread toggle
* Mark all notifications as read
* Automatic notification refresh
* Responsive mobile layout
* Login and logout
* JWT authentication
* User-specific notifications

## Notification Types

The following notification types are supported:

### Like

Created when another user likes the current user's post.

Example:

```text
notification_test liked your post 'Dashboard Test Post'.
```

### Comment

Created when another user comments on the current user's post.

Example:

```text
logesh commented on your post 'Dashboard Test Post'
```

### Subscription

Created when the current user's subscription is activated or renewed.

Example:

```text
Your Basic subscription has been activated successfully.
```

---

# Notification API

## Get Notifications

```http
GET /notifications/
```

Returns notifications belonging to the authenticated user.

## Get Unread Count

```http
GET /notifications/unread-count
```

Returns the number of unread notifications for the authenticated user.

## Mark Notification as Read

```http
PATCH /notifications/{notification_id}/read
```

Marks one notification as read.

## Mark Notification as Unread

```http
PATCH /notifications/{notification_id}/unread
```

Marks one notification as unread.

## Mark All Notifications as Read

```http
PATCH /notifications/read-all
```

Marks all notifications belonging to the authenticated user as read.

---

# Notification Refresh

The React frontend automatically requests the latest notifications every **10 seconds**.

The flow is:

```text
React Frontend
      |
      | Every 10 seconds
      v
FastAPI Notification API
      |
      v
SQLite Database
      |
      v
Updated Notifications
```

This allows newly created notifications to appear without manually refreshing the browser.

> Note: The current implementation uses periodic polling rather than a WebSocket connection. Therefore, notifications are automatically refreshed approximately every 10 seconds rather than being pushed instantly.

---

# Notification Database Model

The notification system stores:

| Field               | Description                     |
| ------------------- | ------------------------------- |
| `id`                | Unique notification ID          |
| `user_id`           | Notification recipient          |
| `message`           | Notification message            |
| `notification_type` | Like, comment, or subscription  |
| `is_read`           | Read/unread state               |
| `created_at`        | Notification creation timestamp |

Notifications are user-specific and protected using JWT authentication.

---

# Post View Tracking

Post views are tracked automatically.

Whenever a user successfully requests:

```http
GET /posts/{post_id}
```

the post's view count is incremented.

The total views for a user's posts are displayed in the User Dashboard.

---

# Authorization

The API implements ownership protection for posts.

For example, if User A creates a post, User B cannot:

* Update User A's post
* Delete User A's post

The API returns:

```text
403 Forbidden
```

with an appropriate error message.

Dashboard and notification data are also protected using JWT authentication.

Users can only access their own dashboard statistics and notifications.

---

# Validation

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

---

# Error Handling

The API handles common errors such as:

```text
400 Bad Request
401 Unauthorized
403 Forbidden
404 Not Found
422 Unprocessable Entity
```

Examples include:

* Invalid login credentials
* Invalid JWT token
* Unauthenticated protected requests
* Post not found
* Unauthorized post modification
* Duplicate like
* Unlike without an existing like
* Subscription limit reached
* Missing active subscription
* Unauthorized notification access

---

# Email Notifications

The API uses Gmail SMTP to send email notifications.

Emails are sent when:

1. A user comments on a post.
2. A user likes a post.

Email credentials are loaded from `.env` using `python-dotenv`.

Email notifications and in-app notifications work independently:

```text
Comment / Like / Subscription Action
             |
       +-----+-----+
       |           |
       v           v
   Email        In-App
Notification   Notification
```

---

# Database

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
* `notifications`

Relationships are configured using SQLAlchemy ORM.

---

# Testing

The API was tested using **Swagger UI**, **Postman**, and the React frontend.

## Backend Testing

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
* Subscription activation
* Subscription renewal
* Subscription limit enforcement
* Billing history
* Invoice generation
* User dashboard statistics
* Dashboard JWT protection
* Post view tracking
* Chart.js dashboard visualization

## Notification Center Testing

The following notification features were tested successfully:

* Notification retrieval
* Like notifications
* Comment notifications
* Subscription notifications
* Unread badge
* Individual notification read
* Individual notification unread
* Mark all as read
* Friendly timestamps
* Automatic 10-second refresh
* Login and logout
* JWT authentication
* Notification persistence
* Responsive mobile layout
* Notification type icons
* Notification type labels

## Frontend Testing

The React notification frontend was tested for:

* Login screen
* Successful authentication
* Logout
* Notification dropdown
* Unread badge
* Read/unread state
* Read All functionality
* Automatic notification refresh without page refresh
* Mobile responsive layout

---

# Postman Collection

The Postman collection is available in the project root:

```text
Blog_Management_API_Postman_Collection.json
```

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
* Notification APIs
* Authentication errors
* Validation errors

---

# Security

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
* User-specific notification access
* Subscription-based access control
* Duplicate-like prevention

---

# Running the Complete Project

The project requires two running applications.

### Terminal 1 — FastAPI Backend

```powershell
cd C:\Users\Welcome\blog-api

venv\Scripts\activate

python -m uvicorn app.main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

### Terminal 2 — React Notification Center

```powershell
cd C:\Users\Welcome\blog-api\blog-notification-frontend

npm install

npm run dev
```

Frontend:

```text
http://localhost:5173
```

---

# Submission Evidence

The following screenshots were captured during testing:

1. Login UI
2. Notification Center
3. Individual notification marked as read
4. Mark all notifications as read
5. Automatic notification refresh without browser refresh
6. Mobile responsive notification UI

The screenshots demonstrate the major frontend notification requirements and responsive behavior.

---

# GitHub Repository

Repository:

```text
<your-github-repository-url>
```

The repository contains:

* FastAPI backend
* React notification frontend
* Database models
* API routers
* Notification service
* Dashboard
* Requirements
* Postman collection
* README documentation

---

# Conclusion

The Blog Management API provides a complete mini blogging platform with authentication, post CRUD operations, ownership authorization, comments, likes/unlikes, image uploads, subscriptions, billing history, email notifications, post view tracking, and a user dashboard.

The project also includes an interactive **In-App Notification Center** with:

* Like notifications
* Comment notifications
* Subscription notifications
* Unread notification badge
* Read/unread controls
* Mark all as read
* Automatic notification refresh
* Notification timestamps
* Responsive React UI
* JWT-based authentication

The backend APIs are documented through Swagger/OpenAPI, and the project has been tested using Swagger UI, Postman, and the React frontend.
