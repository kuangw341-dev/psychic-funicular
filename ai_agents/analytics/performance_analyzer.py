# analytics/performance_analyzer.py

import numpy as np


class PerformanceAnalyzer:

    def __init__(self):
        pass

    # ==================================================

    def sharpe_ratio(self, returns):
        if len(returns) < 2:
            return 0

        avg_return = np.mean(returns)
        std = np.std(returns)
        if std == 0:
            return 0

        return round((avg_return / std) * np.sqrt(252), 2)

    # ==================================================

    def expectancy(self, wins, losses):
        if len(wins) == 0 and len(losses) == 0:
            return 0

        avg_win = np.mean(wins) if len(wins) > 0 else 0
        avg_loss = abs(np.mean(losses)) if len(losses) > 0 else 0
        winrate = len(wins) / (len(wins) + len(losses))
        lossrate = 1 - winrate
        expectancy = (winrate * avg_win) - (lossrate * avg_loss)
        return round(expectancy, 2)