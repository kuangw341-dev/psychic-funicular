class SmartMoneyAgent:

    def __init__(self):
        self.name = "SmartMoneyAgent"

    # ==================================================

    def analyze(self, fast_df, slow_df):
        volume = fast_df["volume"]
        avg_volume = volume.rolling(20).mean().iloc[-1]
        cur_volume = volume.iloc[-1]
        vol_ratio = cur_volume / avg_volume if avg_volume > 0 else 1.0

        open_price = fast_df["open"].iloc[-1]
        close = fast_df["close"].iloc[-1]

        # 动态评分：放量倍数1.5倍以下无效，1.5~3倍线性评分10~25
        if vol_ratio < 1.5:
            return {
                "signal": "HOLD",
                "score": 0,
                "reason": "量能不足"
            }
        # 计算分数：1.5倍给10分，3倍及以上给25分
        score = min(25, 10 + (vol_ratio - 1.5) / 1.5 * 15)
        score = round(score, 2)

        if close > open_price:
            return {
                "signal": "LONG",
                "score": score,
                "reason": f"放量阳线 (倍率{vol_ratio:.2f})"
            }
        elif close < open_price:
            return {
                "signal": "SHORT",
                "score": score,
                "reason": f"放量阴线 (倍率{vol_ratio:.2f})"
            }
        else:
            return {
                "signal": "HOLD",
                "score": 0,
                "reason": "放量十字星"
            }