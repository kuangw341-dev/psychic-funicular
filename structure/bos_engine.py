class BOSEngine:

    def __init__(self, lookback=20):

        self.lookback = lookback

    # ==================================================
    # BOS检测
    # ==================================================

    def detect(self, df):

        highs = df["high"]
        lows = df["low"]
        closes = df["close"]

        recent_high = highs.iloc[
            -self.lookback:-1
        ].max()

        recent_low = lows.iloc[
            -self.lookback:-1
        ].min()

        current_close = closes.iloc[-1]

        # ==================================================
        # Bullish BOS
        # ==================================================

        if current_close > recent_high:

            return {
                "bos": "BULLISH",
                "level": recent_high
            }

        # ==================================================
        # Bearish BOS
        # ==================================================

        elif current_close < recent_low:

            return {
                "bos": "BEARISH",
                "level": recent_low
            }

        return {
            "bos": None,
            "level": None
        }