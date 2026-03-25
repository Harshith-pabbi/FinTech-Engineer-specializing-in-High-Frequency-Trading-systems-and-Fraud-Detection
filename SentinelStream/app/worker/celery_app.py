import os
from celery import Celery

celery_broker_url = os.getenv("CELERY_BROKER_URL", "amqp://guest:guest@localhost:5672//")

celery_app = Celery(
    "worker",
    broker=celery_broker_url,
    include=["app.worker.tasks"]
)

celery_app.conf.task_routes = {
    "app.worker.tasks.send_webhook": "main-queue"
}
