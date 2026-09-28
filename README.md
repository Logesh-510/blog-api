# Blog Management API

A full-stack mini blogging platform built with **FastAPI**, **SQLAlchemy**, **SQLite**, and **React/Vite**.

The application includes authentication, blog posts, comments, likes, subscriptions, notifications, user analytics, and an AI Support Chat.

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

| Technology        | Purpose               |
| ----------------- | --------------------- |
| Python            | Programming           |
| FastAPI           | Backend API           |
| SQLAlchemy        | ORM                   |
| SQLite            | Database              |
| Pydantic          | Validation            |
| JWT               | Authentication        |
| Auth0             | Social authentication |
| Google / Facebook | Social login          |
| React             | Frontend              |
| Vite              | Frontend tooling      |
| Chart.js          | Dashboard charts      |
| Passlib + bcrypt  | Password hashing      |
| SMTP              | Email notifications   |
| Postman / Swagger | API testing           |

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
│   ├── main.py
│   ├── routers/
│   │   ├── auth.py
│   │   ├── posts.py
│   │   ├── comments.py
│   │   ├── likes.py
│   │   ├── subscriptions.py
│   │   ├── dashboard.py
│   │   ├── notifications.py
│   │   └── ai_support.py
│   └── services/
│       └── notification_service.py
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
React → /auth/login → Backend JWT → Protected APIs
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

## Main API Endpoints

| Method | Endpoint                      | Purpose              |
| ------ | ----------------------------- | -------------------- |
| POST   | `/auth/register`              | Register             |
| POST   | `/auth/login`                 | Normal login         |
| POST   | `/auth/auth0-login`           | Auth0 login          |
| GET    | `/auth/me`                    | Current user         |
| GET    | `/posts/`                     | List posts           |
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
