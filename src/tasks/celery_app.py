from celery import Celery
from src.config import settings

celery_instance = Celery(
    "tasks",
    broker=settings.REDIS_URL,
    include=[
        "src.tasks.tasks"
    ]
)

celery_instance.conf.beat_schedule = {
    "name": {
        "task": "booking_today_checkin",
        "schedule": 5   # Можно задать периодичность через crontab (crontab guru - полезный сервис)
    }
}


# ВАЖНО - в реальных проектах воркеров и биты запускают отдельно!