# Blog Management API

A backend REST API for a mini blogging platform built with **FastAPI**, **SQLAlchemy**, and **SQLite**.

The application provides JWT authentication, blog post management, comments, likes/unlikes, image uploads, pagination and search, subscription-based access control, billing history, email notifications, an in-app notification center, post view tracking, a user dashboard with interactive analytics, and an AI Support Chat for user assistance.

A separate **React/Vite frontend** is included for the **User Dashboard, In-App Notification Center, and AI Support Chat**.

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
* Total comments made
* Total likes received
* Total views
* Per-post likes
* Per-post comments
* Per-post views
* Interactive Blog Activity chart
* Chart.js visualization
* Responsive dashboard UI
* JWT-protected dashboard data

### AI Support Chat

* Floating AI Support button accessible from the authenticated frontend
* Interactive chat popup
* User message input
* AI response display
* Scrollable conversation history
* Persistent AI support history
* JWT-protected AI Support API
* User-specific AI chat history
* Mocked/predefined support responses
* FAQ assistance for blog posts
* Subscription assistance
* Billing assistance
* Profile management assistance
* Dashboard assistance
* Comments and likes assistance
* Notification assistance
* Login and authentication assistance
* General help and FAQ responses
* Activity tracking using the database

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
| React            | Frontend user interface         |
| Vite             | React development/build tool    |
| React Chart.js 2 | Chart.js integration with React |
| Lucide React     | Frontend UI icons               |
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
│       ├── notifications.py
│       └── ai_support.py
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
│   │   ├── index.css
│   │   └── main.jsx
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

The React/Vite frontend is located inside:

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

The frontend uses:

* React
* Vite
* Chart.js
* React Chart.js 2
* Lucide React

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

# Run the React Frontend

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
* Track post views
* View notifications
* Mark notifications as read/unread
* Mark all notifications as read
* Test AI Support
* View AI Support history
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

The application provides a user-specific dashboard for personal activity statistics and analytics.

## Dashboard API

```http
GET /user/dashboard/
```

Authentication required.

The dashboard returns:

* Total posts created
* Total comments made by the authenticated user
* Total likes received on the user's posts
* Total views received on the user's posts
* Per-post likes
* Per-post comments
* Per-post views

Each authenticated user can only access their own dashboard data.

## Dashboard Frontend

The dashboard is included in the React/Vite frontend.

Frontend:

```text
http://localhost:5173
```

The dashboard displays:

* Total Posts
* Comments Made
* Likes Received
* Total Views
* Blog Activity chart
* Individual post statistics

The **Blog Activity** chart is implemented using **Chart.js** and displays:

* Posts
* Comments
* Likes
* Views

Dashboard data is loaded dynamically from the authenticated dashboard API.

---

# AI Support Chat

The application includes an AI Support Chat to help users understand and use the blog platform.

The current implementation uses a **mocked/predefined response system** for common questions and stores user conversations in the database.

## AI Support API

### Send a Support Message

```http
POST /api/ai-support/
```

Authentication required.

Example request:

```json
{
  "message": "How do I create a post?"
}
```

The endpoint returns an AI Support response.

### View AI Support History

```http
GET /api/ai-support/history/
```

Authentication required.

Returns the authenticated user's previous AI Support conversations.

## AI Support Topics

The support system provides predefined assistance for:

* Creating posts
* Editing posts
* Deleting posts
* Subscriptions
* Billing
* Profile management
* Dashboard analytics
* Comments
* Likes
* Notifications
* Login and authentication
* Registration
* General FAQs

## AI Support Frontend

The AI Support Chat is available through a floating button in the React frontend.

Features include:

* Floating AI Support button
* Chat popup
* User message input
* AI response display
* Scrollable chat history
* Loading state
* Persistent conversation history
* JWT authentication

The frontend communicates with:

```text
POST /api/ai-support/
```

and:

```text
GET /api/ai-support/history/
```

---

# In-App Notification Center

The project includes an interactive React/Vite notification center.

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

# AI Support Database Model

AI Support conversations are stored for authenticated users.

The AI Support chat model stores:

| Field         | Description                     |
| ------------- | ------------------------------- |
| `id`          | Unique chat record ID           |
| `user_id`     | User who asked the question     |
| `question`    | User's support question         |
| `ai_response` | Generated/mock support response |
| `created_at`  | Conversation timestamp          |

AI Support history is user-specific and protected using JWT authentication.

---

# Post View Tracking

Post views are tracked automatically.

Whenever a user successfully requests:

```http
GET /posts/{post_id}
```

the post's view count is incremented.

The total views for a user's posts are displayed in the User Dashboard.

Per-post view statistics are also displayed in the dashboard.

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

Dashboard, notification, and AI Support data are also protected using JWT authentication.

Users can only access their own:

* Dashboard statistics
* Notifications
* AI Support history

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
* Unauthorized AI Support access

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

    Email       In-App
 Notification  Notification
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
* `ai_support_chats`

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
* Per-post dashboard statistics
* Post view tracking
* Chart.js dashboard visualization
* AI Support message requests
* AI Support predefined responses
* AI Support history
* AI Support JWT protection

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

## User Dashboard Testing

The following dashboard features were tested successfully:

* Dashboard authentication
* User-specific dashboard data
* Total posts
* Comments made
* Likes received
* Total views
* Per-post views
* Per-post comments
* Per-post likes
* Chart.js visualization
* Responsive dashboard layout

## AI Support Testing

The following AI Support features were tested successfully:

* AI Support floating button
* AI Support popup
* User question submission
* AI response display
* Loading state
* Chat history
* History persistence after refresh
* Create post FAQ
* Subscription FAQ
* Dashboard FAQ
* Authentication protection
* User-specific chat history

## Frontend Testing

The React frontend was tested for:

* Login screen
* Successful authentication
* Logout
* User Dashboard
* Dashboard statistics
* Blog Activity chart
* Per-post dashboard statistics
* Notification dropdown
* Unread badge
* Read/unread state
* Read All functionality
* Automatic notification refresh without page refresh
* AI Support floating button
* AI Support chat popup
* AI message submission
* AI response display
* AI history persistence
* Responsive mobile layout

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
* AI Support API
* AI Support history
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
* User-specific AI Support history
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

### Terminal 2 — React Frontend

```powershell
cd C:\Users\Welcome\blog-api\blog-notification-frontend

npm install

npm run dev
```

Frontend:

```text
http://localhost:5173
```

The React frontend provides:

* User Dashboard
* Blog Activity Chart
* In-App Notification Center
* AI Support Chat
* JWT-based authentication

---

# Submission Evidence

The following screenshots were captured during testing:

1. Login UI
2. Notification Center
3. Individual notification marked as read
4. Mark all notifications as read
5. Automatic notification refresh without browser refresh
6. Mobile responsive notification UI
7. User Dashboard
8. Dashboard statistics
9. Blog Activity Chart
10. Per-post dashboard statistics
11. AI Support Chat
12. AI Support responses
13. AI Support history persistence

The screenshots demonstrate the major frontend, dashboard, AI Support, notification, and responsive UI requirements.

---

# GitHub Repository

Repository:

```text
<your-github-repository-url>
```

The repository contains:

* FastAPI backend
* React/Vite frontend
* Database models
* API routers
* Notification service
* Email notification service
* User Dashboard
* AI Support Chat
* Notification Center
* Chart.js visualization
* Requirements
* Postman collection
* README documentation

---

# Conclusion

The Blog Management API provides a complete mini blogging platform with:

* JWT authentication
* User registration and login
* Post CRUD operations
* Ownership authorization
* Comments
* Likes/unlikes
* Multiple image uploads
* Pagination and search
* Subscription plans
* Billing history
* Invoice generation
* Email notifications
* In-app notifications
* Post view tracking
* User dashboard analytics
* Chart.js visualization
* AI Support Chat

The project also includes an interactive **React/Vite frontend** containing:

* User Dashboard
* Blog Activity Chart
* In-App Notification Center
* AI Support Chat
* JWT-based authentication
* Responsive UI

The **User Dashboard** provides authenticated users with personal activity statistics including posts, comments, likes, and views.

The **In-App Notification Center** provides:

* Like notifications
* Comment notifications
* Subscription notifications
* Unread notification badge
* Read/unread controls
* Mark all as read
* Automatic notification refresh
* Notification timestamps
* Responsive React UI

The **AI Support Chat** provides:

* User assistance
* FAQ responses
* Post management guidance
* Subscription and billing assistance
* Dashboard assistance
* Notification assistance
* Persistent conversation history
* User-specific authenticated chat history

The backend APIs are documented through Swagger/OpenAPI, and the project has been tested using Swagger UI, Postman, and the React frontend.
