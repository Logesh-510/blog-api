from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import AISupportChat
from ..schemas import AISupportRequest, AISupportResponse
from ..routers.auth import get_current_user
from ..models import User


router = APIRouter(
    prefix="/api/ai-support",
    tags=["AI Support"]
)


def get_ai_response(message: str) -> str:
    message_lower = message.lower().strip()

    # Create post
    if (
        ("create" in message_lower or "add" in message_lower)
        and "post" in message_lower
    ):
        return (
            "To create a post, log in to your account and open the "
            "Create Post option. Enter your title and content, add "
            "images if your subscription plan allows them, and submit "
            "the post. Your post will be associated with your account."
        )

    # Edit post
    if (
        ("edit" in message_lower or "update" in message_lower)
        and "post" in message_lower
    ):
        return (
            "To edit a post, open the post you own and select the Edit "
            "option. Update the title, content, or supported images and "
            "save your changes."
        )

    # Delete post
    if (
        ("delete" in message_lower or "remove" in message_lower)
        and "post" in message_lower
    ):
        return (
            "To delete a post, open the post you own and select the "
            "Delete option. The post and its associated content will "
            "be removed according to the platform's rules."
        )

    # Subscription
    if (
        "subscription" in message_lower
        or "subscribe" in message_lower
        or "plan" in message_lower
    ):
        return (
            "The platform provides different subscription plans with "
            "different limits for posts, images, likes, and comments. "
            "You can view the available plans and your current plan "
            "from the Subscriptions section. If you reach a plan limit, "
            "you may need to upgrade to continue that activity."
        )

    # Billing
    if (
        "billing" in message_lower
        or "invoice" in message_lower
        or "payment" in message_lower
        or "transaction" in message_lower
    ):
        return (
            "You can view your subscription billing information and "
            "transaction history from the Billing section. Completed "
            "subscription transactions can have an associated invoice."
        )

    # Profile
    if (
        "profile" in message_lower
        or "account" in message_lower
        or "username" in message_lower
        or "email" in message_lower
    ):
        return (
            "Your profile contains your account information such as "
            "username, email, and subscription details. Use the "
            "available profile or account options to manage your "
            "information."
        )

    # Dashboard
    if (
        "dashboard" in message_lower
        or "analytics" in message_lower
        or "statistics" in message_lower
        or "stats" in message_lower
    ):
        return (
            "Your dashboard provides an overview of your blog activity. "
            "It includes total posts, comments made, likes received, "
            "and post views. These analytics help you monitor your "
            "activity on the platform."
        )

    # Comments
    if (
        "comment" in message_lower
        or "comments" in message_lower
    ):
        return (
            "You can add comments to blog posts when your subscription "
            "plan allows comments. Your comments are linked to your "
            "account, and comment activity can contribute to your "
            "dashboard statistics."
        )

    # Likes
    if (
        "like" in message_lower
        or "likes" in message_lower
    ):
        return (
            "You can like blog posts to interact with content from "
            "other users. Likes received on your posts are reflected "
            "in your dashboard analytics. Your subscription plan may "
            "limit how many likes you can give."
        )

    # Notifications
    if (
        "notification" in message_lower
        or "notifications" in message_lower
        or "alert" in message_lower
    ):
        return (
            "Notifications keep you informed about activity related "
            "to your account and posts. You can view your notifications "
            "and manage their read or unread status from the "
            "Notifications section."
        )

    # Login / authentication
    if (
        "login" in message_lower
        or "log in" in message_lower
        or "sign in" in message_lower
        or "password" in message_lower
    ):
        return (
            "Use your registered username and password to log in. "
            "After successful authentication, you can access protected "
            "features such as creating posts, commenting, liking, "
            "subscriptions, and dashboard analytics."
        )

    # Registration
    if (
        "register" in message_lower
        or "registration" in message_lower
        or "sign up" in message_lower
        or "signup" in message_lower
    ):
        return (
            "To create an account, use the registration option and "
            "provide the required username, email, and password. "
            "After registration, you can log in and use the platform."
        )

    # General FAQ / help
    if (
        "help" in message_lower
        or "faq" in message_lower
        or "what can you do" in message_lower
        or "what can i ask" in message_lower
    ):
        return (
            "I'm your Blog Platform AI Support Assistant. I can help "
            "you with creating, editing, and deleting posts, "
            "subscriptions, billing, profile management, dashboard "
            "analytics, comments, likes, notifications, login, "
            "registration, and other general platform questions."
        )

    # Greeting
    if (
        "hello" in message_lower
        or "hi" in message_lower
        or "hey" in message_lower
    ):
        return (
            "Hello! 👋 I'm your Blog Platform AI Support Assistant. "
            "How can I help you today?"
        )

    # Fallback
    return (
        "I'm your Blog Platform AI Support Assistant. I can help you "
        "with posts, subscriptions, billing, profile management, "
        "dashboard analytics, comments, likes, notifications, "
        "authentication, and general platform FAQs. Please ask me "
        "about any of these topics."
    )

@router.post("/", response_model=AISupportResponse)
def ai_support(
    request: AISupportRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    ai_response = get_ai_response(request.message)

    chat = AISupportChat(
        user_id=current_user.id,
        question=request.message,
        ai_response=ai_response
    )

    db.add(chat)
    db.commit()
    db.refresh(chat)

    return chat

@router.get("/history/", response_model=list[AISupportResponse])
def get_ai_support_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    chats = (
        db.query(AISupportChat)
        .filter(AISupportChat.user_id == current_user.id)
        .order_by(AISupportChat.created_at.asc())
        .all()
    )

    return chats