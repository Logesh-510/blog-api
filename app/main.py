from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from .database import Base, engine
from . import models
from .routers import (
    auth,
    posts,
    comments,
    likes,
    subscriptions,
    notifications,
    dashboard as dashboard_router
)
from .routers import ai_support

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Blog Management API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Media directory
MEDIA_DIR = BASE_DIR / "media"

# Serve uploaded images
app.mount(
    "/media",
    StaticFiles(directory=MEDIA_DIR),
    name="media"
)

# Serve User Dashboard
@app.get("/dashboard")
def dashboard():
    return FileResponse(
        BASE_DIR / "dashboard" / "dashboard.html"
    )

# Include routers
app.include_router(auth.router)
app.include_router(posts.router)
app.include_router(comments.router)
app.include_router(likes.router)
app.include_router(subscriptions.router)
app.include_router(notifications.router)
app.include_router(dashboard_router.router)
app.include_router(ai_support.router)

# Root endpoint
@app.get("/")
def root():
    return {
        "message": "Blog Management API is running"
    }
