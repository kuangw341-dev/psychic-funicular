# risk/volatility_risk.py

class VolatilityRisk:

    def __init__(self):
        pass

    # ==================================================

    def evaluate(self, atr, price):
        volatility = atr / price

        # ==================================================

        if volatility > 0.05:
            return {
                "high_risk": True,
                "recommended_leverage": 2
            }

        # ==================================================

        if volatility > 0.03:
            return {
                "high_risk": False,
                "recommended_leverage": 3
            }

        # ==================================================

        return {
            "high_risk": False,
            "recommended_leverage": 5
        }