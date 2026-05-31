# ai_agents/analytics/trade_logger.py

import pandas as pd


class TradeLogger:

    def __init__(self):
        self.logs = []

    # ==================================================

    def log(self, side, entry_price, exit_price, pnl_pct, profit, result, reason, market_regime, entry_time, exit_time):
        self.logs.append({
            "side": side,
            "entry_price": entry_price,
            "exit_price": exit_price,
            "pnl_pct": pnl_pct,
            "profit": profit,
            "result": result,
            "reason": reason,
            "market_regime": market_regime,
            "entry_time": entry_time,
            "exit_time": exit_time
        })

    # ==================================================

    def get_dataframe(self):
        return pd.DataFrame(self.logs)

    # ==================================================

    def export_csv(self, path="trade_logs.csv"):
        df = self.get_dataframe()
        df.to_csv(path, index=False)
        print(f"""

交易记录已导出:

{path}
""")