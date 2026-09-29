# Blog Management API

A full-stack mini blogging platform built with **FastAPI**, **SQLAlchemy**, **SQLite**, and **React/Vite**.

The application includes authentication, blog posts, comments, likes, subscriptions, notifications, user analytics, AI Support Chat, and scheduled blog publishing.

---

## Features

### Authentication

* User registration and login
* JWT authentication
* Login using username or email
* Auth0 social authentication
* Google login
* Facebook login
* Automatic local user creation for Auth0 users
* Protected API endpoints
* Ownership-based authorization

### Blog Management

* Create, view, update, and delete posts
* Multiple image uploads
* Pagination and search
* Post view tracking
* Comments
* Like/unlike
* Duplicate-like prevention

### Scheduled Blog Publishing

Authors can choose how a blog post should be published:

* Publish immediately
* Save as draft
* Schedule for future publishing

Scheduled publishing workflow:

```text
Draft
  ↓
Scheduled
  ↓
Automatic Scheduler
  ↓
Published
```

Features include:

* Future date and time scheduling
* Scheduled post status
* Automatic publishing using APScheduler
* Automatic `published_at` timestamp
* `scheduled_at` cleared after publishing
* Scheduled posts hidden from public post listings until published
* Validation to prevent scheduling in the past
* Draft posts cannot have a scheduled datetime
* Immediate posts cannot have a scheduled datetime
* Scheduler checks for due posts every 10 seconds

### Subscription & Billing

* Basic, Premium, and Pro plans
* Plan-based usage limits
* Subscription activation and renewal
* Billing history
* Invoice generation

### Notifications

* Email notifications
* In-app notification center
* Like, comment, and subscription notifications
* Read/unread controls
* Mark all as read
* Unread notification badge
* Automatic 10-second refresh

### User Dashboard

* Total posts
* Comments made
* Likes received
* Total views
* Per-post statistics
* Blog Activity chart using Chart.js

### AI Support

* Floating support chat
* Predefined FAQ responses
* Post, subscription, billing, dashboard, and notification assistance
* Persistent user-specific chat history

---

## Tech Stack

| Technology        | Purpose                   |
| ----------------- | ------------------------- |
| Python            | Programming               |
| FastAPI           | Backend API               |
| SQLAlchemy        | ORM                       |
| SQLite            | Database                  |
| Pydantic          | Validation                |
| JWT               | Authentication            |
| Auth0             | Social authentication     |
| Google / Facebook | Social login              |
| React             | Frontend                  |
| Vite              | Frontend tooling          |
| Chart.js          | Dashboard charts          |
| Passlib + bcrypt  | Password hashing          |
| SMTP              | Email notifications       |
| APScheduler       | Scheduled blog publishing |
| Postman / Swagger | API testing               |

---

## Project Structure

```text
blog-api/

│
├── app/
│   ├── auth.py
│   ├── database.py
│   ├── dependencies.py
│   ├── models.py
│   ├── schemas.py
│   ├── email_service.py
│   ├── invoice.py
│   ├── main.py
│   │
│   ├── routers/
│   │   ├── auth.py
│   │   ├── posts.py
│   │   ├── comments.py
│   │   ├── likes.py
│   │   ├── subscriptions.py
│   │   ├── dashboard.py
│   │   ├── notifications.py
│   │   └── ai_support.py
│   │
│   └── services/
│       ├── notification_service.py
│       └── scheduler.py
│
├── blog-notification-frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── main.jsx
│   ├── package.json
│   └── package-lock.json
│
├── media/
├── .env
├── .gitignore
├── requirements.txt
├── README.md
└── Blog_Management_API_Postman_Collection.json
```

---

## Installation

### Backend

```powershell
git clone <your-github-repository-url>

cd blog-api

python -m venv venv

venv\Scripts\activate

python -m pip install -r requirements.txt
```

### Frontend

```powershell
cd blog-notification-frontend

npm install
```

---

## Environment Variables

Create `.env` in the project root:

```env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USERNAME=your-email@gmail.com
EMAIL_PASSWORD=your-gmail-app-password
SECRET_KEY=your-secret-key

AUTH0_DOMAIN=your-auth0-domain
AUTH0_CLIENT_ID=your-auth0-client-id
```

**Never commit `.env` or real credentials to GitHub.**

---

## Run the Application

### Backend

```powershell
cd C:\Users\Welcome\blog-api

venv\Scripts\activate

python -m uvicorn app.main:app --reload
```

Backend:

`http://127.0.0.1:8000`

Swagger:

`http://127.0.0.1:8000/docs`

### Frontend

Open another terminal:

```powershell
cd C:\Users\Welcome\blog-api\blog-notification-frontend

npm run dev
```

Frontend:

`http://localhost:5173`

---

## Authentication Flow

### Normal Login

```text
React
  ↓
/auth/login
  ↓
Backend JWT
  ↓
Protected APIs
```

### Auth0 Login

```text
React
  ↓
Auth0
  ↓
Google / Facebook
  ↓
Auth0 ID Token
  ↓
/auth/auth0-login
  ↓
Validate Token
  ↓
Create/Find Local User
  ↓
Backend JWT
  ↓
Protected APIs
```

Auth0 endpoint:

```http
POST /auth/auth0-login
```

---

## Auth0 Configuration

For local development, configure the Auth0 application with:

```text
Allowed Callback URLs:

http://localhost:5173

Allowed Logout URLs:

http://localhost:5173

Allowed Web Origins:

http://localhost:5173
```

Enable:

* Google connection
* Facebook connection

---

## Scheduled Blog Publishing

### Publishing Options

The post creation and update APIs support three publishing options:

| Option     | Status      | Behavior                                            |
| ---------- | ----------- | --------------------------------------------------- |
| `publish`  | `published` | Publishes immediately                               |
| `draft`    | `draft`     | Saves as draft                                      |
| `schedule` | `scheduled` | Publishes automatically at the selected future time |

### Create Scheduled Post

Endpoint:

```http
POST /posts/
```

Example form-data:

```text
title=Future of Artificial Intelligence
content=AI will transform many industries in the coming years.
publish_option=schedule
scheduled_at=2026-09-29T08:41:34
```

When a future `scheduled_at` value is supplied:

```text
status = scheduled
published_at = null
```

### Automatic Publishing

APScheduler runs in the FastAPI application and checks scheduled posts every 10 seconds.

When the scheduled time is reached:

```text
status = scheduled
        ↓
scheduled_at <= current UTC time
        ↓
status = published
published_at = current UTC time
scheduled_at = null
```

Example verified result:

```json
{
    "id": 14,
    "title": "Scheduled Publishing Test",
    "status": "published",
    "scheduled_at": null,
    "published_at": "2026-09-29T08:41:39.674256"
}
```

### Validation Rules

* `scheduled_at` is required when `publish_option` is `schedule`.
* `scheduled_at` must be in the future.
* Past scheduled times are rejected.
* Draft posts cannot have a scheduled datetime.
* Immediately published posts cannot have a scheduled datetime.
* Scheduled posts are not publicly visible until they are published.

### Scheduler

The scheduler implementation is located at:

```text
app/services/scheduler.py
```

The scheduler is started when the FastAPI application starts and stopped when the application shuts down.

---

## Main API Endpoints

| Method | Endpoint                      | Purpose              |
| ------ | ----------------------------- | -------------------- |
| POST   | `/auth/register`              | Register             |
| POST   | `/auth/login`                 | Normal login         |
| POST   | `/auth/auth0-login`           | Auth0 login          |
| GET    | `/auth/me`                    | Current user         |
| GET    | `/posts/`                     | List published posts |
| POST   | `/posts/`                     | Create post          |
| GET    | `/posts/{id}`                 | View post            |
| PUT    | `/posts/{id}`                 | Update post          |
| DELETE | `/posts/{id}`                 | Delete post          |
| POST   | `/posts/{id}/comments/`       | Add comment          |
| POST   | `/posts/{id}/like/`           | Like post            |
| DELETE | `/posts/{id}/like/`           | Unlike post          |
| GET    | `/subscriptions/plans`        | Subscription plans   |
| GET    | `/subscriptions/current`      | Current subscription |
| GET    | `/user/dashboard/`            | User dashboard       |
| GET    | `/notifications/`             | Notifications        |
| GET    | `/notifications/unread-count` | Unread count         |
| POST   | `/api/ai-support/`            | AI Support           |
| GET    | `/api/ai-support/history/`    | AI Support history   |

---

## Testing

The application was tested using:

* Swagger UI
* Postman
* React/Vite frontend
* Normal username/password login
* Auth0 Google login
* Auth0 Facebook login
* Dashboard authentication
* Notification center
* AI Support Chat
* Subscription limits
* Post CRUD and authorization
* Comments and likes
* Email notifications
* Scheduled blog publishing

### Scheduled Publishing Test

The scheduled publishing feature was tested end-to-end.

Test flow:

```text
1. Create scheduled post
        ↓
2. Verify status = scheduled
        ↓
3. Wait until scheduled time
        ↓
4. APScheduler detects the post
        ↓
5. Post automatically changes to published
        ↓
6. published_at timestamp is recorded
```

Verified test:

```text
Post ID: 14

Scheduled time:
2026-09-29T08:41:34 UTC

Published time:
2026-09-29T08:41:39.674256 UTC

Initial status:
scheduled

Final status:
published
```

The scheduled publishing workflow was successfully verified end-to-end.

---

## Security

* Passwords hashed using bcrypt
* JWT-protected APIs
* Auth0 ID token validation
* Auth0 issuer and audience validation
* Protected user-specific data
* Ownership authorization
* Credentials stored in environment variables
* `.env` excluded from Git

---

## License

This project was developed as a **Blog Management API and full-stack application project**.
