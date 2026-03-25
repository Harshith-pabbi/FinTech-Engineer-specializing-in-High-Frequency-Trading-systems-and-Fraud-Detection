import pytest
from app.services.rule_engine import RuleEngine
from app.services.ml_pipeline import ml_model
from app.services.fraud_engine import evaluate_transaction_risk

def test_rule_engine_high_amount():
    engine = RuleEngine()
    # Amount > 5000 should be flagged
    assert engine.evaluate(5001, "retail", "Home", "active") == True
    assert engine.evaluate(4999, "retail", "Home", "active") == False

def test_rule_engine_high_risk_category():
    engine = RuleEngine()
    # Crypto > 1000 should be flagged
    assert engine.evaluate(1500, "crypto", "Home", "active") == True
    assert engine.evaluate(900, "crypto", "Home", "active") == False

def test_rule_engine_inactive_user():
    engine = RuleEngine()
    # Inactive user should be flagged
    assert engine.evaluate(100, "retail", "Home", "suspended") == True

def test_rule_engine_suspicious_location():
    engine = RuleEngine()
    assert engine.evaluate(100, "retail", "Country_X", "active") == True
    
def test_ml_pipeline_model_loaded():
    # Ensure the model is loaded and can predict
    score = ml_model.predict_risk_score(150.0, 5)
    assert 0.0 <= score <= 1.0

@pytest.mark.asyncio
async def test_evaluate_transaction_risk_safe():
    result = await evaluate_transaction_risk(
        amount=50.0,
        category="groceries",
        location="Home",
        user_status="active",
        user_tx_count=10
    )
    # ML model with low amount should be low risk, rules shouldn't flag
    assert result["rule_flagged"] == False
    assert result["is_fraudulent"] == False
    assert 0.0 <= result["risk_score"] <= 1.0

@pytest.mark.asyncio
async def test_evaluate_transaction_risk_fraud():
    # Trigger rule engine to ensure fraudulent
    result = await evaluate_transaction_risk(
        amount=10000.0,
        category="retail",
        location="Home",
        user_status="active",
        user_tx_count=1
    )
    assert result["rule_flagged"] == True
    assert result["is_fraudulent"] == True
