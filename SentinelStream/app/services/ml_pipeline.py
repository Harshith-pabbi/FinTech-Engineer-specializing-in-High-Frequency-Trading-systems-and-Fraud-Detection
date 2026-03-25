import numpy as np
from sklearn.ensemble import IsolationForest
import logging

logger = logging.getLogger(__name__)

class MLFraudModel:
    def __init__(self):
        # Initialize a basic Isolation Forest model
        self.model = IsolationForest(
            n_estimators=100,
            contamination=0.05,
            random_state=42
        )
        # Mock training data to "fit" the model
        X_train = np.random.randn(1000, 2) * 50
        # Add some outliers
        X_train = np.vstack([X_train, np.random.randn(50, 2) * 500])
        self.model.fit(X_train)
        logger.info("ML Fraud Model initialized and fitted with mock data.")

    def predict_risk_score(self, amount: float, user_tx_count: int = 1) -> float:
        try:
            # Create a feature array
            features = np.array([[amount, user_tx_count]])
            
            # score_samples returns negative anomaly scores. Lower = more anomalous.
            score = self.model.score_samples(features)[0]
            
            # Map score to a risk range:
            normalized_risk = 1.0 - ((score + 1.0) / 1.5)
            
            # Clip between 0 and 1
            final_risk = max(0.0, min(1.0, normalized_risk))
            return round(final_risk, 3)
        except Exception as e:
            logger.error(f"Error predicting risk score: {e}")
            return 0.5

ml_model = MLFraudModel()
