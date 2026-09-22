from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..dependencies import get_current_user
from ..models import User, Post, Comment, Like
from ..schemas import DashboardResponse, DashboardPostStats


router = APIRouter(
    prefix="/user",
    tags=["Dashboard"]
)


@router.get("/dashboard/", response_model=DashboardResponse)
def get_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # Total posts created by the current user
    total_posts = db.query(Post).filter(
        Post.author_id == current_user.id
    ).count()

    # Total comments made by the current user
    total_comments = db.query(Comment).filter(
        Comment.user_id == current_user.id
    ).count()

    # Total likes received on the current user's posts
    total_likes_received = db.query(Like).join(
        Post,
        Like.post_id == Post.id
    ).filter(
        Post.author_id == current_user.id
    ).count()

    # Total views received on the current user's posts
    user_posts = db.query(Post).filter(
        Post.author_id == current_user.id
    ).all()

    total_views = sum(
        post.views for post in user_posts
    )

    # Per-post statistics
    post_stats = []

    for post in user_posts:
        post_stats.append(
            DashboardPostStats(
                post_id=post.id,
                title=post.title,
                likes=len(post.likes),
                comments=len(post.comments)
            )
        )

    return {
        "total_posts": total_posts,
        "total_comments": total_comments,
        "total_likes_received": total_likes_received,
        "total_views": total_views,
        "posts": post_stats
    }
