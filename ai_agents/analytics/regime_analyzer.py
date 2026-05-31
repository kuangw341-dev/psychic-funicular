# analytics/regime_analyzer.py

class RegimeAnalyzer:

    def __init__(self):
        self.records = {
            "TREND": [],
            "RANGE": [],
            "VOLATILE": []
        }

    # ==================================================

    def record(self, regime, profit):
        if regime not in self.records:
            self.records[regime] = []
        self.records[regime].append(profit)

    # ==================================================

    def analyze(self):
        output = {}

        # ==================================================

        for regime, profits in self.records.items():
            total = sum(profits)
            trades = len(profits)
            avg = 0
            if trades > 0:
                avg = total / trades

            output[regime] = {
                "total_profit": round(total, 2),
                "trades": trades,
                "avg_profit": round(avg, 2)
            }

        # ==================================================

        return output