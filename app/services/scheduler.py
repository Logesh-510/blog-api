from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session

from ..database import SessionLocal
from ..models import Post


scheduler = BackgroundScheduler()


def publish_scheduled_posts():
    """
    Publish all scheduled posts whose scheduled time has arrived.
    """

    db: Session = SessionLocal()

    try:
        now = datetime.utcnow()

        scheduled_posts = (
            db.query(Post)
            .filter(
                Post.status == "scheduled",
                Post.scheduled_at.isnot(None),
                Post.scheduled_at <= now,
            )
            .all()
        )

        for post in scheduled_posts:
            post.status = "published"
            post.published_at = now
            post.scheduled_at = None

        if scheduled_posts:
            db.commit()

            print(
                f"[Scheduler] Published "
                f"{len(scheduled_posts)} scheduled post(s)."
            )

    except Exception as error:
        db.rollback()

        print(
            f"[Scheduler] Error while publishing scheduled posts: "
            f"{error}"
        )

    finally:
        db.close()


def start_scheduler():
    """
    Start the background scheduler.
    """

    if not scheduler.running:

        scheduler.add_job(
            publish_scheduled_posts,
            "interval",
            seconds=10,
            id="publish_scheduled_posts",
            replace_existing=True,
        )

        scheduler.start()

        print(
            "[Scheduler] Scheduled publishing scheduler started."
        )


def stop_scheduler():
    """
    Stop the background scheduler.
    """

    if scheduler.running:
        scheduler.shutdown()

        print(
            "[Scheduler] Scheduled publishing scheduler stopped."
        )