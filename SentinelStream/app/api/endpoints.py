from fastapi import APIRouter, Depends, Header, Request, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.transaction import TransactionRequest, TransactionResponse
from app.services.idempotency import check_idempotency, save_idempotency_response
from app.services.fraud_engine import evaluate_transaction_risk
from app.db.models import FactTransaction
from app.worker.tasks import send_webhook
import uuid

router = APIRouter()

@router.post("/transaction", response_model=TransactionResponse)
async def process_transaction(
    request: Request,
    payload: TransactionRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    idempotency_key = request.headers.get("idempotency-key")
    
    # 1. Idempotency Check
    if idempotency_key:
        cached_response = await check_idempotency(idempotency_key)
        if cached_response:
            return TransactionResponse(**cached_response)

    user_tx_count = 5 # Mock count
    
    # 2. Parallel evaluation
    risk_result = await evaluate_transaction_risk(
        amount=payload.amount,
        category=payload.category,
        location=payload.location,
        user_status=payload.user_status,
        user_tx_count=user_tx_count
    )
    
    is_fraudulent = risk_result["is_fraudulent"]
    risk_score = risk_result["risk_score"]
    
    status = "declined" if is_fraudulent else "approved"
    tx_id = str(uuid.uuid4())
    
    # 3. Write to PostgreSQL
    new_tx = FactTransaction(
        id=tx_id,
        user_id=payload.user_id,
        merchant_id=payload.merchant_id,
        amount=payload.amount,
        currency=payload.currency,
        status=status,
        risk_score=risk_score,
        is_fraudulent=is_fraudulent
    )
    db.add(new_tx)
    await db.commit()
    
    # 4. Async Webhook
    send_webhook.delay(tx_id, status, risk_score)
    
    response_data = {
        "transaction_id": tx_id,
        "status": status,
        "risk_score": risk_score,
        "message": "Transaction declined due to high risk." if is_fraudulent else "Transaction approved."
    }
    
    # 5. Save Idempotency
    if idempotency_key:
        background_tasks.add_task(save_idempotency_response, idempotency_key, response_data)
        
    return TransactionResponse(**response_data)
