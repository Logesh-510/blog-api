from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..invoice import generate_invoice
from ..dependencies import get_current_user
from ..models import BillingHistory, SubscriptionPlan, User
from ..services.notification_service import create_notification

router = APIRouter(
    prefix="/subscriptions",
    tags=["Subscriptions"]
)


@router.get("/plans")
def get_subscription_plans(
    db: Session = Depends(get_db)
):
    plans = db.query(SubscriptionPlan).all()

    return [
        {
            "id": plan.id,
            "name": plan.name,
            "price": plan.price,
            "max_posts": plan.max_posts,
            "max_images_per_post": plan.max_images_per_post,
            "max_likes": plan.max_likes,
            "max_comments": plan.max_comments
        }
        for plan in plans
    ]


@router.get("/current")
def get_current_subscription(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.subscription_plan_id is None:
        return {
            "message": "You do not have an active subscription."
        }

    plan = db.query(SubscriptionPlan).filter(
        SubscriptionPlan.id == current_user.subscription_plan_id
    ).first()

    if plan is None:
        raise HTTPException(
            status_code=404,
            detail="Active subscription plan not found."
        )

    latest_billing = (
        db.query(BillingHistory)
        .filter(BillingHistory.user_id == current_user.id)
        .order_by(BillingHistory.created_at.desc())
        .first()
    )

    return {
        "plan": {
            "id": plan.id,
            "name": plan.name,
            "price": plan.price,
            "max_posts": plan.max_posts,
            "max_images_per_post": plan.max_images_per_post,
            "max_likes": plan.max_likes,
            "max_comments": plan.max_comments
        },
        "billing": {
            "start_date": latest_billing.start_date
            if latest_billing else None,
            "end_date": latest_billing.end_date
            if latest_billing else None,
            "transaction_id": latest_billing.transaction_id
            if latest_billing else None,
            "invoice_path": latest_billing.invoice_path
            if latest_billing else None
        }
    }

@router.post("/subscribe/{plan_id}")
def subscribe_to_plan(
    plan_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    is_renewal = current_user.subscription_plan_id is not None
    plan = db.query(SubscriptionPlan).filter(
        SubscriptionPlan.id == plan_id
    ).first()

    if plan is None:
        raise HTTPException(
            status_code=404,
            detail="Subscription plan not found."
        )

    start_date = datetime.utcnow()
    end_date = start_date + timedelta(days=30)

    transaction_id = (
        f"TXN-{current_user.id}-"
        f"{int(start_date.timestamp())}"
    )

    # Generate invoice PDF
    invoice_path = generate_invoice(
        username=current_user.username,
        plan_name=plan.name,
        price=plan.price,
        start_date=start_date,
        end_date=end_date,
        transaction_id=transaction_id
    )

    # Activate subscription
    current_user.subscription_plan_id = plan.id

    # Save billing history
    billing = BillingHistory(
        user_id=current_user.id,
        subscription_plan_id=plan.id,
        price=plan.price,
        start_date=start_date,
        end_date=end_date,
        transaction_id=transaction_id,
        invoice_path=invoice_path
    )

    db.add(billing)
    db.commit()
    db.refresh(billing)

    create_notification(
        db=db,
        user_id=current_user.id,
        message=(
            f"Your {plan.name} subscription has been "
            f"{'renewed' if is_renewal else 'activated'} successfully."
        ),
        notification_type="subscription"
    )
    
    return {
        "message": (
            f"{plan.name} subscription "
            f"{'renewed' if is_renewal else 'activated'} successfully."
        ),
        "subscription": {
            "plan": plan.name,
            "price": plan.price,
            "start_date": start_date,
            "end_date": end_date,
            "transaction_id": transaction_id,
            "invoice_path": invoice_path
        }
    }