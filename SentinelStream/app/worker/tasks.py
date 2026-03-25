from app.worker.celery_app import celery_app
import requests
import logging

logger = logging.getLogger(__name__)

@celery_app.task(name="app.worker.tasks.send_webhook")
def send_webhook(transaction_id: str, status: str, risk_score: float = None):
    """
    Sends an async webhook notification.
    """
    logger.info(f"Sending webhook for transaction {transaction_id} with status {status}")
    
    payload = {
        "transaction_id": transaction_id,
        "status": status,
        "risk_score": risk_score
    }
    
    webhook_url = "http://httpbin.org/post"
    
    try:
        response = requests.post(webhook_url, json=payload, timeout=5.0)
        response.raise_for_status()
        logger.info(f"Webhook sent successfully: {response.status_code}")
        return True
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to send webhook: {e}")
        return False
