from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..dependencies import get_current_user
from ..models import Like, Post, SubscriptionPlan, User
from ..schemas import LikeResponse
from ..services.notification_service import send_like_notification


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
    background_tasks: BackgroundTasks,
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

    # Check active subscription
    if current_user.subscription_plan_id is None:
        raise HTTPException(
            status_code=403,
            detail="You need an active subscription to like posts."
        )

    plan = db.query(SubscriptionPlan).filter(
        SubscriptionPlan.id == current_user.subscription_plan_id
    ).first()

    if plan is None:
        raise HTTPException(
            status_code=404,
            detail="Active subscription plan not found."
        )

    # Check like limit
    if plan.max_likes is not None:
        like_count = db.query(Like).filter(
            Like.user_id == current_user.id
        ).count()

        if like_count >= plan.max_likes:
            raise HTTPException(
                status_code=403,
                detail="You’ve reached your plan limit. Kindly upgrade your plan to continue."
            )

    # Check if user already liked the post
    existing_like = db.query(Like).filter(
        Like.post_id == post_id,
        Like.user_id == current_user.id
    ).first()

    if existing_like:
        raise HTTPException(
            status_code=400,
            detail="You have already liked this post"
        )

    # Create like
    new_like = Like(
        post_id=post_id,
        user_id=current_user.id
    )

    db.add(new_like)
    db.commit()
    db.refresh(new_like)

    # Send notification in the background
    background_tasks.add_task(
        send_like_notification,
        recipient_email=post.author.email,
        post_title=post.title,
        user_name=current_user.username,
        action_time=new_like.created_at
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
