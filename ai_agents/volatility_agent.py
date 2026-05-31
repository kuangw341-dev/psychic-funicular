class VolatilityAgent:

    def __init__(self):
        self.name = "VolatilityAgent"

    # ==================================================

    def analyze(self, fast_df, slow_df):
        high = fast_df["high"]
        low = fast_df["low"]
        close = fast_df["close"]

        atr = (high - low).rolling(14).mean().iloc[-1]
        avg_atr = (high - low).rolling(50).mean().iloc[-1]

        # 波动扩大条件
        if atr > avg_atr * 1.2:
            # 根据价格相对EMA20的方向决定多空
            ema20 = close.ewm(span=20).mean().iloc[-1]
            current_price = close.iloc[-1]
            if current_price > ema20:
                return {
                    "signal": "LONG",
                    "score": 15,
                    "reason": "波动扩大 + 价格在EMA20之上"
                }
            elif current_price < ema20:
                return {
                    "signal": "SHORT",
                    "score": 15,
                    "reason": "波动扩大 + 价格在EMA20之下"
                }
            else:
                return {
                    "signal": "HOLD",
                    "score": 0,
                    "reason": "波动扩大但价格持平EMA"
                }
        else:
            return {
                "signal": "HOLD",
                "score": 0,
                "reason": "波动正常"
            }