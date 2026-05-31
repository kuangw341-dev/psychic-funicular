class PullbackAgent:

    def __init__(self):
        self.name = "PullbackAgent"

    # ==================================================

    def analyze(self, fast_df, slow_df):
        close = fast_df["close"]
        ema20 = close.ewm(span=20).mean().iloc[-1]
        current_price = close.iloc[-1]
        # 动态阈值：ATR调整或固定0.5%
        atr = (fast_df["high"] - fast_df["low"]).rolling(14).mean().iloc[-1]
        dynamic_threshold = max(0.003, atr / current_price * 0.5)  # 至少0.3%
        distance = abs(current_price - ema20) / ema20

        # 趋势方向（使用EMA20与EMA50关系）
        ema50 = close.ewm(span=50).mean().iloc[-1]
        trend_up = (ema20 > ema50)
        trend_down = (ema20 < ema50)

        if distance <= dynamic_threshold:
            if current_price > ema20 and trend_up:
                return {
                    "signal": "LONG",
                    "score": 20,
                    "reason": f"回踩EMA20 (距离{distance:.4f})"
                }
            elif current_price < ema20 and trend_down:
                return {
                    "signal": "SHORT",
                    "score": 20,
                    "reason": f"跌破EMA20 (距离{distance:.4f})"
                }
            else:
                return {
                    "signal": "HOLD",
                    "score": 0,
                    "reason": "回踩但趋势不匹配"
                }
        else:
            return {
                "signal": "HOLD",
                "score": 0,
                "reason": "无回踩机会"
            }