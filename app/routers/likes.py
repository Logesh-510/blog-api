from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..dependencies import get_current_user
from ..email import send_email
from ..models import Like, Post, User
from ..schemas import LikeResponse


router = APIRouter(
    prefix="/posts/{post_id}/like",
    tags=["Likes"]
)


@router.post(
    "/",
    response_model=LikeResponse,
    status_code=status.HTTP_201_CREATED
)
def like_post(
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

    existing_like = db.query(Like).filter(
        Like.post_id == post_id,
        Like.user_id == current_user.id
    ).first()

    if existing_like:
        raise HTTPException(
            status_code=400,
            detail="You have already liked this post"
        )

    new_like = Like(
        post_id=post_id,
        user_id=current_user.id
    )

    db.add(new_like)
    db.commit()
    db.refresh(new_like)

    send_email(
        recipient=post.author.email,
        subject=f"New like on your post: {post.title}",
        body=(
            f"Hello {post.author.username},\n\n"
            f"{current_user.username} liked your post.\n\n"
            f"Post: {post.title}\n\n"
            f"Regards,\n"
            f"Blog Management API"
        )
    )

    return new_like

@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT
)
def unlike_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    like = db.query(Like).filter(
        Like.post_id == post_id,
        Like.user_id == current_user.id
    ).first()

    if not like:
        raise HTTPException(
            status_code=404,
            detail="You have not liked this post"
        )

    db.delete(like)
    db.commit()

    return None