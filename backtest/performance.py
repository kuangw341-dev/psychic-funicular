# V50_CORE/backtest/performance.py

import numpy as np


class Performance:

    def __init__(self):
        pass

    # ==================================================
    # Winrate
    # ==================================================

    def winrate(self, wins, total):
        if total == 0:
            return 0
        return round((wins / total) * 100, 2)

    # ==================================================
    # Profit Factor
    # ==================================================

    def profit_factor(self, total_profit, total_loss):
        if total_loss == 0:
            return 0
        return round(total_profit / total_loss, 2)

    # ==================================================
    # Max Drawdown
    # ==================================================

    def max_drawdown(self, equity_curve):
        peak = equity_curve[0]
        max_dd = 0
        for value in equity_curve:
            if value > peak:
                peak = value
            dd = (peak - value) / peak
            if dd > max_dd:
                max_dd = dd
        return round(max_dd * 100, 2)

    # ==================================================
    # Sharpe Ratio
    # ==================================================

    def sharpe_ratio(self, returns):
        if len(returns) < 2:
            return 0
        avg_return = np.mean(returns)
        std_return = np.std(returns)
        if std_return == 0:
            return 0
        sharpe = (avg_return / std_return) * np.sqrt(252)
        return round(sharpe, 2)

    # ==================================================
    # Sortino Ratio
    # ==================================================

    def sortino_ratio(self, returns):
        if len(returns) < 2:
            return 0
        downside = [r for r in returns if r < 0]
        if len(downside) == 0:
            return 0
        avg_return = np.mean(returns)
        downside_std = np.std(downside)
        if downside_std == 0:
            return 0
        sortino = (avg_return / downside_std) * np.sqrt(252)
        return round(sortino, 2)

    # ==================================================
    # Expectancy
    # ==================================================

    def expectancy(self, wins, losses):
        if len(wins) == 0 and len(losses) == 0:
            return 0
        avg_win = np.mean(wins) if len(wins) > 0 else 0
        avg_loss = abs(np.mean(losses)) if len(losses) > 0 else 0
        total = len(wins) + len(losses)
        winrate = len(wins) / total
        lossrate = 1 - winrate
        expectancy = (winrate * avg_win) - (lossrate * avg_loss)
        return round(expectancy, 2)

    # ==================================================
    # Recovery Factor
    # ==================================================

    def recovery_factor(self, net_profit, max_drawdown):
        if max_drawdown == 0:
            return 0
        return round(net_profit / max_drawdown, 2)

    # ==================================================
    # Monte Carlo
    # ==================================================

    def monte_carlo(self, returns, simulations=100):
        if len(returns) == 0:
            return {
                "best": 0,
                "worst": 0,
                "average": 0
            }
        results = []
        for _ in range(simulations):
            shuffled = np.random.permutation(returns)
            results.append(np.sum(shuffled))
        return {
            "best": round(max(results), 2),
            "worst": round(min(results), 2),
            "average": round(np.mean(results), 2)
        }