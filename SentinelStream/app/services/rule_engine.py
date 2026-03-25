class RuleEngine:
    def evaluate(self, amount: float, category: str, location: str, user_status: str) -> bool:
        """
        Evaluate static rules for fraud detection.
        Returns True if the transaction is flagged as fraudulent by rules.
        """
        # Rule 1: Abnormally high transaction amount
        if amount > 5000:
            return True
            
        # Rule 2: High risk category with significant amount
        if category.lower() in ["crypto", "jewelry", "wire_transfer"] and amount > 1000:
            return True
            
        # Rule 3: User account not active
        if user_status.lower() != "active":
            return True
            
        # Rule 4: Suspicious locations
        high_risk_locations = ["Country_X", "Country_Y"]
        if location in high_risk_locations:
            return True
            
        return False
