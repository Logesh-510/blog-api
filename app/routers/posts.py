import os
import uuid
from math import ceil

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    Query,
    UploadFile,
    status
)
from sqlalchemy.orm import Session

from ..database import get_db
from ..dependencies import get_current_user
from ..models import Post, User
from ..schemas import PaginatedPostResponse, PostResponse


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


# Image upload directory
MEDIA_DIR = "media/posts"
os.makedirs(MEDIA_DIR, exist_ok=True)


@router.post(
    "/",
    response_model=PostResponse,
    status_code=status.HTTP_201_CREATED
)
def create_post(
    title: str = Form(...),
    content: str = Form(...),
    image: UploadFile | None = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    image_path = None

    if image:
        file_extension = os.path.splitext(image.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(MEDIA_DIR, unique_filename)

        with open(file_path, "wb") as buffer:
            buffer.write(image.file.read())

        image_path = f"/media/posts/{unique_filename}"

    new_post = Post(
        title=title,
        content=content,
        image=image_path,
        author_id=current_user.id
    )

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get(
    "/",
    response_model=PaginatedPostResponse
)
def get_posts(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    search: str | None = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Post)

    # Search by title or content
    if search:
        search_term = f"%{search}%"

        query = query.filter(
            Post.title.ilike(search_term) |
            Post.content.ilike(search_term)
        )

    # Total number of matching posts
    total = query.count()

    # Calculate total pages
    total_pages = ceil(total / limit) if total > 0 else 0

    # Calculate starting position
    offset = (page - 1) * limit

    # Get paginated posts
    posts = (
        query
        .order_by(Post.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    return {
        "posts": posts,
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": total_pages
    }


@router.get(
    "/{post_id}",
    response_model=PostResponse
)
def get_post(
    post_id: int,
    db: Session = Depends(get_db)
):
    post = db.query(Post).filter(
        Post.id == post_id
    ).first()

    if not post:
        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )

    return post


@router.put(
    "/{post_id}",
    response_model=PostResponse
)
def update_post(
    post_id: int,
    title: str = Form(...),
    content: str = Form(...),
    image: UploadFile | None = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    post = db.query(Post).filter(
        Post.id == post_id
    ).first()

    if not post:
        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )

    if post.author_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You can only update your own posts"
        )

    post.title = title
    post.content = content

    # Replace image if a new image is uploaded
    if image:
        file_extension = os.path.splitext(image.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(MEDIA_DIR, unique_filename)

        with open(file_path, "wb") as buffer:
            buffer.write(image.file.read())

        post.image = f"/media/posts/{unique_filename}"

    db.commit()
    db.refresh(post)

    return post


@router.delete(
    "/{post_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    post = db.query(Post).filter(
        Post.id == post_id
    ).first()

    if not post:
        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )

    if post.author_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You can only delete your own posts"
        )

    db.delete(post)
    db.commit()

    return None
