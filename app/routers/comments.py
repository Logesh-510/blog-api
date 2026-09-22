from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..dependencies import get_current_user
from ..models import Comment, Post, SubscriptionPlan, User
from ..schemas import CommentCreate, CommentResponse
from ..services.notification_service import send_comment_notification

router = APIRouter(
    prefix="/posts/{post_id}/comments",
    tags=["Comments"]
)


@router.post(
    "/",
    response_model=CommentResponse,
    status_code=status.HTTP_201_CREATED
)
def create_comment(
    post_id: int,
    comment_data: CommentCreate,
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
            detail="You need an active subscription to comment."
        )

    plan = db.query(SubscriptionPlan).filter(
        SubscriptionPlan.id == current_user.subscription_plan_id
    ).first()

    if plan is None:
        raise HTTPException(
            status_code=404,
            detail="Active subscription plan not found."
        )

    # Check comment limit
    if plan.max_comments is not None:
        comment_count = db.query(Comment).filter(
            Comment.user_id == current_user.id
        ).count()

        if comment_count >= plan.max_comments:
            raise HTTPException(
                status_code=403,
                detail="You’ve reached your plan limit. Kindly upgrade your plan to continue."
            )

    new_comment = Comment(
        post_id=post_id,
        user_id=current_user.id,
        text=comment_data.text
    )

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    background_tasks.add_task(
        send_comment_notification,
        recipient_email=post.author.email,
        post_title=post.title,
        user_name=current_user.username,
        action_time=new_comment.created_at
    )
    return new_comment

@router.get(
    "/",
    response_model=list[CommentResponse]
)
def get_comments(
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

    comments = db.query(Comment).filter(
        Comment.post_id == post_id
    ).order_by(
        Comment.created_at.asc()
    ).all()

    return comments
