class TrendAgent:

    def __init__(self):
        self.name = "TrendAgent"

    # ==================================================

    def analyze(self, fast_df, slow_df):
        fast_df["ema20"] = fast_df["close"].ewm(span=20).mean()
        fast_df["ema50"] = fast_df["close"].ewm(span=50).mean()

        ema20 = fast_df["ema20"].iloc[-1]
        ema50 = fast_df["ema50"].iloc[-1]
        close = fast_df["close"].iloc[-1]

        # 计算均线距离（相对于价格）
        distance = abs(ema20 - ema50) / close
        # 动态分数：距离0.003以下给15分，0.003~0.01线性增加至25分，超过0.01给25分
        if distance < 0.003:
            base_score = 15
        else:
            base_score = min(25, 15 + (distance - 0.003) / 0.007 * 10)

        if ema20 > ema50:
            return {
                "signal": "LONG",
                "score": round(base_score, 2),
                "reason": f"EMA20 > EMA50 上升趋势 (距离{distance:.4f})"
            }
        elif ema20 < ema50:
            return {
                "signal": "SHORT",
                "score": round(base_score, 2),
                "reason": f"EMA20 < EMA50 下降趋势 (距离{distance:.4f})"
            }
        else:
            return {
                "signal": "HOLD",
                "score": 0,
                "reason": "趋势不明确"
            }