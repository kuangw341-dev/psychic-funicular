class ShadowLearning:

    def __init__(self):
        self.records = []

    # ==================================================

    def add_record(self, real_profit, shadow_profit):
        missed = shadow_profit - real_profit
        self.records.append({
            "real_profit": real_profit,
            "shadow_profit": shadow_profit,
            "missed_profit": missed
        })

    # ==================================================

    def analyze(self):
        if len(self.records) == 0:
            return {
                "tp_too_early": False,
                "avg_missed_profit": 0
            }

        missed_list = [r["missed_profit"] for r in self.records]
        avg_missed = sum(missed_list) / len(missed_list)

        # ==================================================

        return {
            "tp_too_early": avg_missed > 0.03,
            "avg_missed_profit": avg_missed
        }