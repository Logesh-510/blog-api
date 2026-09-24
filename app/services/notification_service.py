from datetime import datetime

from sqlalchemy.orm import Session

from .email_service import send_email
from ..models import Notification

def create_notification(
    db: Session,
    user_id: int,
    message: str,
    notification_type: str
):
    notification = Notification(
        user_id=user_id,
        message=message,
        notification_type=notification_type,
        is_read=0
    )

    db.add(notification)
    db.commit()
    db.refresh(notification)

    return notification

def send_comment_notification(
    recipient_email: str,
    post_title: str,
    user_name: str,
    action_time: datetime
):
    subject = "New Comment on Your Post"

    body = f"""Hello,

Someone commented on your blog post.

Post: "{post_title}"
User: {user_name}
Activity: Commented on your post
Time: {action_time.strftime("%Y-%m-%d %I:%M %p")}

Regards,
Blog Management API
"""

    send_email(
        recipient_email=recipient_email,
        subject=subject,
        body=body
    )


def send_like_notification(
    recipient_email: str,
    post_title: str,
    user_name: str,
    action_time: datetime
):
    subject = "Someone Liked Your Post"

    body = f"""Hello,

Someone liked your blog post.

Post: "{post_title}"
User: {user_name}
Activity: Liked your post
Time: {action_time.strftime("%Y-%m-%d %I:%M %p")}

Regards,
Blog Management API
"""

    send_email(
        recipient_email=recipient_email,
        subject=subject,
        body=body
    )
