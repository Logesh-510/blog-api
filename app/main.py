from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .database import Base, engine
from . import models
from .routers import auth, posts, comments, likes, subscriptions


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Blog Management API",
    version="1.0.0"
)


# Serve uploaded images
BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_DIR = BASE_DIR / "media"

app.mount("/media", StaticFiles(directory=MEDIA_DIR), name="media")


app.include_router(auth.router)
app.include_router(posts.router)
app.include_router(comments.router)
app.include_router(likes.router)
app.include_router(subscriptions.router)

@app.get("/")
def root():
    return {
        "message": "Blog Management API is running"
    }