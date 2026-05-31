# analytics/agent_analyzer.py

class AgentAnalyzer:

    def __init__(self):
        self.records = {}

    # ==================================================

    def record(self, agent_name, profit):
        if agent_name not in self.records:
            self.records[agent_name] = []
        self.records[agent_name].append(profit)

    # ==================================================

    def analyze(self):
        result = {}

        # ==================================================

        for agent, profits in self.records.items():
            total = sum(profits)
            wins = len([p for p in profits if p > 0])
            total_trades = len(profits)
            winrate = 0
            if total_trades > 0:
                winrate = (wins / total_trades) * 100

            result[agent] = {
                "total_profit": round(total, 2),
                "trades": total_trades,
                "winrate": round(winrate, 2)
            }

        # ==================================================

        return result