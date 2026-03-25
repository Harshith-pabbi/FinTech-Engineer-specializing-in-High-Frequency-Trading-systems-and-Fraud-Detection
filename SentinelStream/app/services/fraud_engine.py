import asyncio
from app.services.ml_pipeline import ml_model
from app.services.rule_engine import RuleEngine

rule_engine = RuleEngine()

async def evaluate_transaction_risk(
    amount: float, 
    category: str, 
    location: str, 
    user_status: str, 
    user_tx_count: int = 1
) -> dict:
    """
    Runs the ML model and Rule Engine in parallel.
    """
    loop = asyncio.get_running_loop()
    
    ml_task = loop.run_in_executor(
        None, 
        ml_model.predict_risk_score, 
        amount, 
        user_tx_count
    )
    
    rule_task = loop.run_in_executor(
        None,
        rule_engine.evaluate,
        amount,
        category,
        location,
        user_status
    )
    
    # Wait for both tasks
    ml_score, rule_flagged = await asyncio.gather(ml_task, rule_task)
    
    # Final determination:
    # Flag as fraudulent if rules catch it OR if ML model strongly thinks it's anomalous (>0.85)
    is_fraudulent = rule_flagged or (ml_score > 0.85)
    
    return {
        "risk_score": ml_score,
        "rule_flagged": rule_flagged,
        "is_fraudulent": is_fraudulent
    }
